import re
import types
from copy import copy

from django import template
from django.core.exceptions import ImproperlyConfigured
from django.template.base import FILTER_SEPARATOR, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from .. import settings

register = template.Library()


def silence_without_field(fn):
    """
    Args:
        fn:
    """

    def wrapped(field, attr):
        if not field:
            return ""
        return fn(field, attr)

    return wrapped


def _process_field_attributes(field, attr, process):

    # split attribute name and value from 'attr:value' string
    """
    Args:
        field:
        attr:
        process:
    """
    params = attr.split(":", 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ""

    field = copy(field)

    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


@register.filter("attr")
@silence_without_field
def set_attr(field, attr):
    """
    Args:
        field:
        attr:
    """

    def process(widget, attrs, attribute, value):
        attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter("append_attr")
@silence_without_field
def append_attr(field, attr):
    """
    Args:
        field:
        attr:
    """

    def process_str(field, attr):
        params = attr.split(":", 1)
        attribute = params[0]
        value = params[1] if len(params) == 2 else ""

        content = field.split("name")
        content.insert(1, f'{attribute}="{value}" name')
        field = "".join(content)
        return mark_safe(field)

    if isinstance(field, str):
        return process_str(field, attr)

    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += " " + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + " " + value
        else:
            attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter("add_class")
@silence_without_field
def add_class(field, css_class):
    """
    Args:
        field:
        css_class:
    """
    return append_attr(field, "class:" + css_class)


@register.filter("data")
@silence_without_field
def set_data(field, data):
    return set_attr(field, "data-" + data)


@register.filter(name="field_type")
def field_type(field):
    """Template filter that returns field class name (in lower case). E.g. if
    field is CharField then {{ field|field_type }} will return 'charfield'.

    Args:
        field:
    """
    if hasattr(field, "field") and field.field:
        return field.field.__class__.__name__.lower()
    return ""


@register.filter(name="widget_name")
def widget_name(field):
    """Template filter that returns field widget class name (in lower case).
    E.g. if field's widget is TextInput then {{ field|widget_type }} will return
    'textinput'.

    Args:
        field:
    """
    if (
        hasattr(field, "field")
        and hasattr(field.field, "widget")
        and field.field.widget
    ):
        return field.field.widget.__class__.__name__.lower()
    return ""


# ======================== render_field tag ==============================

ATTRIBUTE_RE = re.compile(
    r"""
    (?P<attr>
        [\w_-]+
    )
    (?P<sign>
        \+?=
    )
    (?P<value>
    ['"]? # start quote
        [^"']*
    ['"]? # end quote
    )
""",
    re.VERBOSE | re.UNICODE,
)

# ATTRIBUTE_RE = re.compile(r"""(?P<attr>[\w_-]+)(?P<sign>\+?=)(?P<value>['"]?[^"']*['"]?)""", re.VERBOSE | re.UNICODE)


@register.tag
def render_field(parser, token):
    """Render a form field using given attribute-value pairs

    Takes form field as first argument and list of attribute-value pairs for
    all other arguments. Attribute-value pairs should be in the form of
    attribute=value or attribute="a value" for assignment and attribute+=value
    or attribute+="value" for appending.

    Args:
        parser:
        token:
    """
    error_msg = (
        '%r tag requires a form field followed by a list of attributes and values in the form attr="value"'
        % token.split_contents()[0]
    )
    try:
        bits = token.split_contents()
        tag_name = bits[0]
        form_field = bits[1]
        attr_list = bits[2:]
    except ValueError:
        raise TemplateSyntaxError(error_msg)

    form_field = parser.compile_filter(form_field)

    attrs = []
    for pair in attr_list:
        match = ATTRIBUTE_RE.match(pair)
        if not match:
            raise TemplateSyntaxError(error_msg + ": %s" % pair)
        dct = match.groupdict()
        attr, value = dct["attr"], parser.compile_filter(dct["value"])
        attrs.append((attr, value))

    return FieldNode(form_field, attrs)


class FieldNode(Node):
    def __init__(self, field, attrs):
        """
        Args:
            field:
            attrs:
        """
        self.field = field
        self.attrs = attrs

    def render(self, context):
        """
        Args:
            context:
        """

        bounded_field = self.field.resolve(context)
        # field = getattr(bounded_field, "field", None)
        with context.push():
            for key, value in self.attrs:
                if key == "class":
                    bounded_field = add_class(bounded_field, value.resolve(context))
                elif key == "type":
                    bounded_field.field.widget.input_type = value.resolve(context)
                else:
                    bounded_field = set_attr(
                        bounded_field, "%s:%s" % (key, value.resolve(context))
                    )
                    context.update({key: value.resolve(context)})

            # Get template name
            if not bounded_field:
                raise ImproperlyConfigured("The field passed do not exist.")

            widget_name = bounded_field.widget_type
            if not widget_name in settings.TEMPLATE_WIDGETS:
                if not "default" in settings.TEMPLATE_WIDGETS:
                    raise ImproperlyConfigured(
                        f"Does not exist template name for '{widget_name}' or default widget template."
                    )
                template_name = settings.TEMPLATE_WIDGETS.get("default")
            else:
                template_name = settings.TEMPLATE_WIDGETS.get(widget_name)

            context.update(
                {
                    "field": bounded_field,
                }
            )

            if (
                widget_name in ("clearablefile",)
                and hasattr(bounded_field.form, "instance")
                and hasattr(bounded_field.form.instance, bounded_field.name)
            ):
                file = getattr(bounded_field.form.instance, bounded_field.name)
                if file:
                    context.update({"file_name": file.name, "file_url": file.url})

            t = context.template.engine.get_template(template_name)
            component = t.render(context)
            context.pop()
            return mark_safe(component)

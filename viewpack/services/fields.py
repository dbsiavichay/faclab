from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.forms.utils import pretty_name
from django.utils.html import format_html


class FieldService:
    FIELD_SEPARATOR = "__"
    LABEL_SEPARATOR = ":"

    @classmethod
    def get_field_label(cls, model, field):
        try:
            name, verbose_name = field.split(cls.LABEL_SEPARATOR)
            return pretty_name(verbose_name)
        except ValueError:
            pass

        if "__str__" in field:
            label = str(model._meta.verbose_name)
            return pretty_name(label)

        names = field.split(cls.FIELD_SEPARATOR)
        name = names.pop(0)

        if not hasattr(model, name):
            model_name = (
                model._meta.model_name
                if hasattr(model, "_meta")
                else str(model)  # Model name
            )
            raise AttributeError(
                "Does not exist attribute <{0}> for {1}".format(
                    name,
                    model_name,
                )
            )

        try:
            field = model._meta.get_field(name)

            if len(names):
                related_model = field.related_model
                return cls.get_field_label(
                    related_model, cls.FIELD_SEPARATOR.join(names)
                )
            label = field.verbose_name
        except FieldDoesNotExist:
            attr = getattr(object, name)

            if len(names):
                return cls.get_field_label(
                    attr(model) if callable(attr) else attr,
                    cls.FIELD_SEPARATOR.join(names),
                )
            label = name

        return pretty_name(label)

    @classmethod
    def get_field_value(cls, object, field):
        if object is None or "__str__" in field:
            return object

        field = field.split(cls.LABEL_SEPARATOR)[0]
        names = field.split(cls.FIELD_SEPARATOR)
        name = names.pop(0)

        if not hasattr(object, name):
            raise AttributeError(
                "Does not exist attribute <{0}> for {1}".format(
                    name,
                    str(object),
                )
            )

        if len(names):
            attr = getattr(object, name)
            attr = attr() if callable(attr) else attr

            return cls.get_field_value(
                attr,
                cls.FIELD_SEPARATOR.join(names),
            )

        try:
            field = object._meta.get_field(name)

            if hasattr(field, "choices") and field.choices:
                return dict(field.choices).get(field.value_from_object(object))
            elif field.related_model:
                if field.one_to_many or field.many_to_many:
                    raise ImproperlyConfigured(
                        "OneToMany or ManyToMany is not supported: '%s'"
                        % field.name  # For performace
                    )

                try:
                    return field.related_model.objects.get(
                        pk=field.value_from_object(object)
                    )
                except field.related_model.DoesNotExist:
                    return None
            else:
                return field.value_from_object(object)
        except FieldDoesNotExist:
            attr = getattr(object, name)
            attr = attr() if callable(attr) else attr

            return format_html(str(attr))

    @classmethod
    def get_field_type(cls, model, field):
        field = field.split(cls.LABEL_SEPARATOR)[0]
        names = field.split(cls.FIELD_SEPARATOR)
        name = names.pop(0)

        if not hasattr(model, name):
            model_name = (
                model._meta.model_name
                if hasattr(model, "_meta")
                else str(model)  # Model name
            )
            raise AttributeError(
                "Does not exist attribute <{0}> on {1}".format(
                    name,
                    model_name,
                )
            )

        if len(names):
            if hasattr(model, "_meta"):
                return cls.get_field_type(
                    model._meta.get_field(name).related_model,
                    cls.FIELD_SEPARATOR.join(names),
                )
            else:
                attr = getattr(model, name)
                attr = attr() if callable(attr) else attr
                return cls.get_field_type(
                    attr,
                    cls.FIELD_SEPARATOR.join(names),
                )

        try:
            field = model._meta.get_field(name)
            type = model._meta.get_field(name).get_internal_type()
        except FieldDoesNotExist:
            type = "str"

        return type

    @classmethod
    def get_field_data(cls, object, field):
        return (
            cls.get_field_label(object, field),
            cls.get_field_value(object, field),
            cls.get_field_type(object, field),
        )

    @classmethod
    def get_botstrap_fields(cls, field_names, fields_data):
        def wrap(fields):
            fields = fields if isinstance(fields, (list, tuple)) else (fields,)
            cols = int(12 / len(fields))

            return [fields_data.get(field, ()) + (cols,) for field in fields]

        data = list(map(wrap, field_names))

        return data

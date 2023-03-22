from functools import reduce

from django.contrib.admin.utils import flatten
from django.core.exceptions import FieldDoesNotExist
from django.forms.utils import pretty_name
from django.utils.html import format_html


class FieldService:
    JSON_SPLITTER = "__"

    @classmethod
    def get_field_labels(cls, model, field_names, default_labels):
        labels = []

        for name in field_names:
            label = (
                default_labels.get(name)
                if name in default_labels
                else cls.get_field_label(model, name)
            )
            labels.append((name, label))

        return labels

    @classmethod
    def get_field_label(cls, model, field_name):
        if "__str__" in field_name:
            label = str(model._meta.verbose_name)
            return pretty_name(label)

        names = field_name.split(cls.JSON_SPLITTER)
        name = names.pop(0)

        try:
            field = model._meta.get_field(name)
            label = field.verbose_name
        except FieldDoesNotExist:
            label = field_name

        return pretty_name(label)

    @classmethod
    def get_field_value(cls, object, field_name):
        if object is None or "__str__" in field_name:
            return object

        names = field_name.split(cls.JSON_SPLITTER)
        name = names.pop(0)
        value = (
            object.get(name)
            if isinstance(object, dict)
            else getattr(object, name, None)
        )
        value = value() if callable(value) else value

        if value is None:
            raise AttributeError(
                "Does not exist attribute <{0}> for {1}".format(
                    name,
                    str(object),
                )
            )

        if len(names) and isinstance(value, dict):
            return cls.get_field_value(
                value,
                cls.JSON_SPLITTER.join(names),
            )

        try:
            field = object._meta.get_field(name)
            internal_type = field.get_internal_type()

            if hasattr(field, "choices") and field.choices:
                value = dict(field.choices).get(value)

            return value, internal_type
        except (FieldDoesNotExist, AttributeError):
            return format_html(str(value)), type(value)

    @classmethod
    def get_field_data(cls, object, field):
        return (cls.get_field_label(object, field), *cls.get_field_value(object, field))

    @classmethod
    def get_flatten_field_names(cls, field_names):
        if isinstance(field_names, dict):
            field_names = reduce(
                lambda accumulator, names: accumulator + flatten(names),
                field_names.values(),
                [],
            )
        else:
            field_names = flatten(field_names)

        return field_names

    @classmethod
    def get_botstrap_fields(cls, field_names, fields_data):
        def wrap(fields):
            fields = fields if isinstance(fields, (list, tuple)) else (fields,)
            cols = int(12 / len(fields))

            return [fields_data.get(field, ()) + (cols,) for field in fields]

        data = list(map(wrap, field_names))

        return data

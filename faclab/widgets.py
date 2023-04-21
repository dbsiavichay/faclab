from django import forms
from django_select2.cache import cache
from django_select2.forms import ModelSelect2Widget


class PriceInput(forms.NumberInput):
    input_type = "price"


class PercentInput(forms.NumberInput):
    input_type = "percent"


class DisabledNumberInput(forms.NumberInput):
    input_type = "disablednumber"


class Select2(ModelSelect2Widget):
    input_type = "select2"
    extra_data = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "extra_data" in kwargs:
            self.extra_data = kwargs.pop("extra_data")

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs["data-minimum-input-length"] = 0

        return attrs

    def get_extra_data(self, obj):
        data = {}

        for name in self.extra_data:
            attr = getattr(obj, name, None)

            if attr:
                data[name] = attr

        return data

    def set_to_cache(self):
        queryset = self.get_queryset()
        cache.set(
            self._get_cache_key(),
            {
                "queryset": [queryset.none(), queryset.query],
                "cls": self.__class__,
                "search_fields": tuple(self.search_fields),
                "max_results": int(self.max_results),
                "url": str(self.get_url()),
                "dependent_fields": dict(self.dependent_fields),
                "extra_data": tuple(self.extra_data),
            },
        )

from functools import reduce

from django.contrib.admin.utils import flatten
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import DetailView as BaseDetailView
from django.views.generic import View

from ..services.fields import FieldService
from .base import get_base_view


class DetailMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.pack.detail_extra_context)
        flatten_results, fieldset_results = self.get_results()
        data = {
            "results": fieldset_results,
            "flatten_results": flatten_results,
        }

        if "pack" in context:
            context["pack"].update(data)
        else:
            context.update({"pack": data})

        return context

    def get_results(self):
        if isinstance(self.pack.detail_fields, (list, tuple)):
            fields = flatten(self.pack.detail_fields)
        elif isinstance(self.pack.detail_fields, dict):
            fields = reduce(
                lambda acc, fieldset: acc + flatten(fieldset),
                self.pack.detail_fields.values(),
                [],
            )
        else:
            raise ImproperlyConfigured(
                "The fieldsets must be an instance of list, tuple or dict"
            )
        fields = fields if fields else (field.name for field in self.model._meta.fields)
        results = {
            field: (
                FieldService.get_field_label(self.object, field),
                FieldService.get_field_value(self.object, field),
                FieldService.get_field_type(self.object, field),
            )
            for field in fields
        }

        flatten_results = results.values()

        def parse(fieldset):
            def wrap(fields):
                fields = fields if isinstance(fields, (list, tuple)) else [fields]
                return {
                    "bs_cols": int(12 / len(fields)),
                    "fields": [results.get(field, ("", "", "")) for field in fields],
                }

            fieldset_list = list(map(wrap, fieldset))
            return fieldset_list

        fieldsets_list = self.pack.detail_fields
        fieldsets = (
            [(None, fieldsets_list)]
            if isinstance(fieldsets_list, (list, tuple))
            else fieldsets_list.items()
        )
        fieldsets_results = [
            {"title": title or "", "fieldset": parse(fieldset)}
            for title, fieldset in fieldsets
        ]

        return flatten_results, fieldsets_results


class DetailView(View):
    pack = None

    def view(self, request, *args, **kwargs):
        mixins = [DetailMixin]
        View = get_base_view(BaseDetailView, mixins, self.pack)
        View.__bases__ = (*self.pack.detail_mixins, *View.__bases__)

        view = View.as_view()
        return view(request, *args, **kwargs)

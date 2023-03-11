from functools import reduce

from django.contrib.admin.utils import flatten
from django.views.generic import DetailView as BaseDetailView
from django.views.generic import View

from viewpack.enums import PackViews
from viewpack.services import FieldService

from .base import get_base_view


class DetailMixin:
    name = PackViews.DETAIL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields_data = self.get_fields_data()
        fieldsets_data = self.get_fieldsets_data(fields_data)
        pack_info = context.get("pack_info", {})
        pack_info.update(
            {
                "fields": fields_data.values(),
                "bs_fielsets": fieldsets_data,
            }
        )
        context["pack_info"] = pack_info

        return context

    def get_fieldsets_data(self, fields_data):
        field_names = self.pack.detail_fields

        if not field_names:
            field_names = fields_data.keys()

        fieldsets = (
            field_names.items()
            if isinstance(field_names, dict)
            else [("", field_names)]
        )

        data = [
            {
                "title": title,
                "fieldset": FieldService.get_botstrap_fields(
                    fieldset,
                    fields_data,
                ),
            }
            for title, fieldset in fieldsets
        ]

        return data

    def get_fields_data(self):
        field_names = self.pack.detail_fields
        field_names = (
            field_names
            if field_names
            else (field.name for field in self.model._meta.fields)
        )

        if isinstance(field_names, dict):
            field_names = reduce(
                lambda acc, names: acc + flatten(names),
                field_names.values(),
                [],
            )
        else:
            field_names = flatten(field_names)

        data = {
            name: FieldService.get_field_data(self.object, name)
            for name in field_names  # Data {"attr": (label, value, type)}
        }

        return data


class DetailView(View):
    pack = None

    def view(self, request, *args, **kwargs):
        mixins = [DetailMixin]
        View = get_base_view(BaseDetailView, mixins, self.pack)
        View.__bases__ = (*self.pack.detail_mixins, *View.__bases__)

        view = View.as_view()
        return view(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return self.view(request, *args, **kwargs)

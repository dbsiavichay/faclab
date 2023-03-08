from django.views.generic import ListView as BaseListView
from django.views.generic import View

from ..services.fields import FieldService
from .base import get_base_view


class ListMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.pack.list_extra_context)

        data = {
            "fields": self.get_list_fields(),
            "rows": self.get_rows(context["object_list"]),
            "page_start_index": context["page_obj"].start_index()
            if context["is_paginated"]
            else 1,
            "page_end_index": context["page_obj"].end_index()
            if context["is_paginated"]
            else context["object_list"].count(),
            "total_records": context["paginator"].count
            if context["is_paginated"]
            else context["object_list"].count(),
        }

        if "pack" in context:
            context["pack"].update(data)
        else:
            context.update({"pack": data})

        return context

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get("paginate_by")

        if paginate_by:
            return paginate_by

        return super().get_paginate_by(queryset)

    def get_list_fields(self):
        fields = [
            (name, FieldService.get_field_label(self.model, name))
            for name in self.pack.list_fields
        ]
        return fields

    def get_rows(self, queryset):
        rows = [
            {
                "instance": instance,
                "values": self.get_values(instance),
                # "urls": get_urls_of_site(
                #    self.pack, object=instance, user=self.request.user
                # ),
            }
            for instance in queryset
        ]
        return rows

    def get_values(self, instance):
        values = [
            FieldService.get_field_value(instance, name)
            for name in self.pack.list_fields
        ]
        return values


class ListView(View):
    def view(self, request, *args, **kwargs):
        mixins = [ListMixin]
        View = get_base_view(BaseListView, mixins, self.pack)
        View.paginate_by = self.pack.paginate_by
        View.__bases__ = (*self.pack.list_mixins, *View.__bases__)
        view = View.as_view()

        return view(request, *args, **kwargs)

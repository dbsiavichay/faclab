from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.urls import path
from django_select2.views import AutoResponseView


class Select2View(AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get("term", request.GET.get("term", ""))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        results = [
            {
                "text": self.widget.label_from_instance(obj),
                "id": obj.pk,
                **self.widget.get_extra_data(obj),
            }
            for obj in context["object_list"]
        ]

        return JsonResponse(
            {
                "results": results,
                "more": context["page_obj"].has_next(),
            },
            encoder=DjangoJSONEncoder,
        )


app_name = "django_select2"

urlpatterns = [
    path("fields/auto.json", Select2View.as_view(), name="auto-json"),
]

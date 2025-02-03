from dependency_injector.wiring import Provide, inject
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from apps.core.application.services import SealifyService

from .forms import CertificateForm


class CertificateListView(TemplateView):
    template_name = "base/base_list.html"

    @inject
    def __init__(
        self,
        sealify_service: SealifyService = Provide["core_package.sealify_service"],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.sealify_service = sealify_service

    def get_context_data(self, **kwargs):
        certificates = self.sealify_service.list_certificates()
        context = super().get_context_data(**kwargs)
        pack_info = {
            "headers": {
                "subject_name": "Sujeto",
                "serial_number": "Número de serie",
                "issue_date": "Fecha de emisión",
                "expiry_date": "Fecha de expiración",
            },
            "rows": [
                (
                    obj,
                    {
                        "data": {
                            "subject_name": {
                                "value": obj.subject_name,
                                "label": "Sujeto",
                                "type": "charfield",
                            },
                            "serial_number": {
                                "value": obj.serial_number,
                                "label": "Número de serie",
                                "type": "charfield",
                            },
                            "issue_date": {
                                "value": obj.issue_date,
                                "label": "Fecha de emisión",
                                "type": "datetimefield",
                            },
                            "expiry_date": {
                                "value": obj.expiry_date,
                                "label": "Fecha de expiración",
                                "type": "datetimefield",
                            },
                        },
                        "paths": {
                            "delete": reverse_lazy(
                                "certificate_delete", kwargs={"pk": obj.id}
                            ),
                        },
                    },
                )
                for obj in certificates
            ],
            "paths": {
                "list": reverse_lazy("certificate_list"),
                "create": reverse_lazy("certificate_create"),
            },
            "start_index": 1,
            "end_index": 1,
            "count": len(certificates),
        }
        context["object_list"] = certificates
        context["pack_info"] = pack_info
        return context


class CertificateCreateView(FormView):
    template_name = "base/base_form.html"
    form_class = CertificateForm
    success_url = reverse_lazy("certificate_list")

    @inject
    def __init__(
        self,
        sealify_service: SealifyService = Provide["core_package.sealify_service"],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.sealify_service = sealify_service

    def form_valid(self, form):
        certificate = form.upload_file
        password = form.cleaned_data["signature_password"]
        self.sealify_service.create_certificate(certificate, password)
        return super().form_valid(form)


class CertificateDeleteView(TemplateView):
    template_name = "base/base_confirm_delete.html"
    success_url = reverse_lazy("certificate_list")

    @inject
    def __init__(
        self,
        sealify_service: SealifyService = Provide["core_package.sealify_service"],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.sealify_service = sealify_service

    def post(self, request, pk, *args, **kwargs):
        self.sealify_service.delete_certificate(pk)
        return HttpResponseRedirect(self.success_url)

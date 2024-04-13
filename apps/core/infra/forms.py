from cryptography.hazmat.primitives.serialization import pkcs12
from dependency_injector.wiring import Provide, inject
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from apps.core.domain.enums import Emissions, Environments
from apps.core.domain.models import Signature, Site
from apps.core.domain.repositories import SiteRepository
from apps.sale.application.validators import customer_code_validator
from apps.sri.application.services import SRISigner
from faclab.widgets import PercentInput
from viewpack.forms import ModelForm


class SignatureForm(ModelForm):
    signature_file = forms.FileField(
        validators=[FileExtensionValidator(["p12"])], label=_("signature file")
    )
    signature_password = forms.CharField(
        max_length=256, widget=forms.PasswordInput, label=_("signature password")
    )

    class Meta:
        model = Signature
        fieldsets = ("signature_file", "signature_password")

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("signature_file")
        password = cleaned_data.get("signature_password")

        if file and password:
            try:
                p12_data = file.read()
                pkcs12.load_pkcs12(p12_data, password.encode())
            except ValueError:
                raise ValidationError(_("signature file or password are invalid"))

            data = SRISigner.get_signature_metadata(p12_data, password)
            exists = Signature.objects.filter(
                serial_number=data.get("serial_number")
            ).exists()

            if exists:
                raise ValidationError(_("signature file has already been registered"))

            cleaned_data["metadata"] = data

        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        data = self.cleaned_data.get("metadata")

        for key, value in data.items():
            setattr(obj, key, value)

        if commit:
            obj.save()

        return obj


class SiteForm(ModelForm):
    @inject
    def __init__(
        self,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.site_repository = site_repository

    company_code = forms.CharField(
        max_length=13,
        min_length=13,
        validators=[customer_code_validator],
        label=_("ruc"),
    )
    company_name = forms.CharField(max_length=64, label=_("company name"))
    company_trade_name = forms.CharField(max_length=64, label=_("company trade name"))
    company_main_address = forms.CharField(label=_("company main address"))
    company_branch_address = forms.CharField(label=_("company branch address"))
    company_branch_code = forms.CharField(max_length=4, label=_("company branch code"))
    company_sale_point_code = forms.CharField(
        max_length=4, label=_("company point sale code")
    )
    special_taxpayer_resolution = forms.CharField(
        max_length=32, required=False, label=_("special taxpayer resolution")
    )
    withholding_agent_resolution = forms.CharField(
        max_length=32, required=False, label=_("withholding agent resolution")
    )
    company_accounting_required = forms.BooleanField(
        required=False, label=_("company accounting required")
    )
    environment = forms.ChoiceField(
        choices=Environments.choices,
        initial=Environments.TESTING,
        label=_("type of environment"),
    )
    emission_type = forms.ChoiceField(
        choices=Emissions.choices, initial=Emissions.NORMAL, label=_("type of emission")
    )
    iva_percent = forms.FloatField(widget=PercentInput, label=_("iva percent"))
    signature = forms.ModelChoiceField(
        Signature.objects.all(), required=False, label=_("electronic signature")
    )

    class Meta:
        model = Site
        fieldsets = (
            "company_code",
            ("company_name", "company_trade_name"),
            "company_main_address",
            "company_branch_address",
            ("company_branch_code", "company_sale_point_code"),
            "special_taxpayer_resolution",
            "withholding_agent_resolution",
            "company_accounting_required",
            ("environment", "emission_type"),
            "iva_percent",
            "signature",
        )

    def save(self, commit=True):
        obj = super().save(commit=False)
        data = {**self.cleaned_data}
        signature = data.get("signature")

        if signature:
            data["signature"] = signature.id

        obj.sri_config = data

        if commit:
            obj.save()

        self.site_repository.refresh_site()

        return obj

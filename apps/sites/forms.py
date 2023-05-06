from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from apps.sales.validators import customer_code_validator
from faclab.widgets import PercentInput
from viewpack.forms import ModelForm

from .enums import Emissions, Environments
from .models import Config


class ConfigForm(ModelForm):
    code = forms.CharField(
        max_length=13,
        min_length=13,
        validators=[customer_code_validator],
        label=_("ruc"),
    )
    company_name = forms.CharField(max_length=64, label=_("company name"))
    trade_name = forms.CharField(max_length=64, label=_("trade name"))
    main_address = forms.CharField(label=_("main address"))
    company_address = forms.CharField(label=_("company address"))
    company_code = forms.CharField(max_length=4, label=_("company code"))
    company_point_sale_code = forms.CharField(
        max_length=4, label=_("company point sale code")
    )
    special_taxpayer_resolution = forms.CharField(
        max_length=32, required=False, label=_("special taxpayer resolution")
    )
    withholding_agent_resolution = forms.CharField(
        max_length=32, required=False, label=_("withholding agent resolution")
    )
    accounting_required = forms.BooleanField(
        required=False, label=_("accounting required")
    )
    environment = forms.ChoiceField(
        choices=Environments.choices,
        initial=Environments.TESTING,
        label=_("type of environment"),
    )
    emission = forms.ChoiceField(
        choices=Emissions.choices, initial=Emissions.NORMAL, label=_("type of emission")
    )
    iva_percent = forms.FloatField(widget=PercentInput, label=_("iva percent"))

    signature_file = forms.FileField(
        validators=[FileExtensionValidator("p12")], label=_("signature file")
    )
    signature_password = forms.CharField(
        max_length=256, widget=forms.PasswordInput, label=_("signature password")
    )

    class Meta:
        model = Config
        fieldsets = {
            _("company settings"): (
                "code",
                ("company_name", "trade_name"),
                "main_address",
                "company_address",
                ("company_code", "company_point_sale_code"),
                "special_taxpayer_resolution",
                "withholding_agent_resolution",
                "accounting_required",
                ("environment", "emission"),
                "iva_percent",
            ),
            _("electronic invoicing"): (
                "signature_file",
                "signature_password",
            ),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        data = {**self.cleaned_data}
        file = data.pop("signature_file")
        file_path = default_storage.save(file.name, ContentFile(file.read()))
        data["signature_file"] = file_path
        obj.sri_config = data

        if commit:
            obj.save()

        return obj

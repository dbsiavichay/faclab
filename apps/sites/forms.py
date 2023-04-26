from django import forms
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

    class Meta:
        model = Config
        fieldsets = (
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
        )

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.sri_config = self.cleaned_data

        if commit:
            obj.save()

        return obj

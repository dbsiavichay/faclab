from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from viewpack.forms import ModelForm

from .models import Customer
from .validators import customer_code_validator


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fieldsets = (
            ("code_type", "code"),
            ("first_name", "last_name"),
            "bussiness_name",
            "address",
            ("phone", "email"),
        )

    def clean(self):
        cleaned_data = super().clean()
        code_type = cleaned_data.get("code_type")
        code = cleaned_data.get("code")

        if code_type and code:
            long = len(code)

            if code_type.length != long:
                raise ValidationError(
                    _("The code entered does not correspond to a %(code_type)s"),
                    params={"code_type": code_type.name},
                )

            if code_type.code in ("04", "05"):
                customer_code_validator(code)

        return cleaned_data

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from viewpack.forms import ModelForm

from .enums import CodeTypes
from .models import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        code_type = cleaned_data.get("code_type")
        code = cleaned_data.get("code")

        if code_type and code:
            long = len(code)
            valids = {CodeTypes.CHARTER: 10, CodeTypes.RUC: 13}

            if valids.get(code_type) != long:
                raise ValidationError(
                    _("The code entered does not correspond to a %(code_type)s"),
                    params={"code_type": CodeTypes(code_type).label.upper()},
                )

        return cleaned_data

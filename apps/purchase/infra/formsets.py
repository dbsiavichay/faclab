from dependency_injector.wiring import Provide, inject
from django import forms

from apps.purchase.application.services import PurchaseService
from apps.purchase.domain.entities import PurchaseEntity

from .forms import PurchaseLineForm
from .models import Purchase, PurchaseLine


class PurchaseLineInlineFormset(forms.BaseInlineFormSet):
    @inject
    def __init__(
        self,
        purchase_service: PurchaseService = Provide[
            "purchase_package.purchase_service"
        ],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.purchase_service = purchase_service

    def save(self, commit=True):
        object_list = super().save(commit=commit)
        purchase_entity = PurchaseEntity(**self.instance.__dict__)
        self.purchase_service.update_purchase_total(purchase_entity)
        update_fields = ["subtotal", "tax", "total"]
        self.instance.__dict__.update(purchase_entity.model_dump(include=update_fields))
        self.instance.save()

        return object_list


PurchaseLineFormset = forms.inlineformset_factory(
    Purchase,
    PurchaseLine,
    form=PurchaseLineForm,
    formset=PurchaseLineInlineFormset,
    extra=1,
    # min_num=1,
    # validate_min=True,
)

from dependency_injector.wiring import Provide, inject
from django import forms

from apps.inventory.application.services import PurchaseService
from apps.inventory.domain.choices import PriceTypes
from apps.inventory.domain.entities import PurchaseEntity

from .forms import ProductPriceForm, PurchaseLineForm
from .models import Product, ProductPrice, Purchase, PurchaseLine


class ProductPriceInlineFormset(forms.BaseInlineFormSet):
    def get_queryset(self):
        return super().get_queryset().filter(type=PriceTypes.SALE)


class PurchaseLineInlineFormset(forms.BaseInlineFormSet):
    @inject
    def __init__(
        self,
        purchase_service: PurchaseService = Provide[
            "inventory_package.purchase_service"
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


ProductPriceFormset = forms.inlineformset_factory(
    Product,
    ProductPrice,
    form=ProductPriceForm,
    formset=ProductPriceInlineFormset,
    extra=1,
)


PurchaseLineFormset = forms.inlineformset_factory(
    Purchase,
    PurchaseLine,
    form=PurchaseLineForm,
    formset=PurchaseLineInlineFormset,
    extra=1,
    # min_num=1,
    # validate_min=True,
)

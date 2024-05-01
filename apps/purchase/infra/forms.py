from dependency_injector.wiring import Provide, inject
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.inventory.infra.models import Product
from apps.inventory.infra.querysets import ProductQueryset
from apps.purchase.application.services import PurchaseService
from apps.purchase.domain.entities import PurchaseLineEntity
from faclab.widgets import DisabledNumberInput, PriceInput, Select2
from viewpack.forms import ModelForm

from .models import Provider, Purchase, PurchaseLine


class ProviderForm(ModelForm):
    class Meta:
        model = Provider
        fieldsets = (
            "code",
            ("bussiness_name", "contact_name"),
            "address",
            ("phone", "email", "website"),
        )


class PurchaseForm(ModelForm):
    products = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Product.objects.all(),
        widget=Select2(
            model="inventory.Product",
            search_fields=[
                "code__icontains",
                "name__icontains",
            ],
        ),
        label=_("product search"),
    )

    class Meta:
        model = Purchase
        fieldsets = ("provider", ("date", "invoice_number"))
        fields = ("products",)
        widgets = {
            "provider": Select2(
                model="purchase.Provider",
                search_fields=[
                    "code__icontains",
                    "bussiness_name__icontains",
                    "contact_name__icontains",
                ],
            )
        }


class PurchaseLineForm(ModelForm):
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

    subtotal = forms.FloatField(
        widget=DisabledNumberInput, required=False, label=_("subtotal")
    )

    class Meta:
        model = PurchaseLine
        fields = ("product", "quantity", "unit_price", "subtotal")
        widgets = {
            "unit_price": PriceInput,
            "product": Select2(
                queryset=ProductQueryset.product_with_first_cost_price,
                search_fields=["name__icontains"],
                extra_data=("first_cost_price",),
            ),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        purchaseline_entity = PurchaseLineEntity(**obj.__dict__)
        self.purchase_service.update_purchase_line_total(purchaseline_entity)
        obj.__dict__.update(
            purchaseline_entity.model_dump(include=["subtotal", "tax", "total"])
        )

        if commit:
            obj.save()

        return obj

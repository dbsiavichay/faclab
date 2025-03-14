from dependency_injector.wiring import Provide, inject
from rest_framework import serializers

from apps.core.domain.repositories import SiteRepository
from apps.inventory.infra.serializers import ProductSerializer

from .models import Invoice, InvoiceLine, InvoicePayment


class SRIConfigSerializer(serializers.Serializer):
    company_code = serializers.CharField(max_length=13)
    company_name = serializers.CharField()
    company_trade_name = serializers.CharField()
    company_main_address = serializers.CharField()
    company_branch_address = serializers.CharField()
    company_branch_code = serializers.CharField(max_length=4)
    company_sale_point_code = serializers.CharField(max_length=4)
    special_taxpayer_resolution = serializers.CharField(allow_null=True, required=False)
    withholding_agent_resolution = serializers.CharField(
        allow_null=True, required=False
    )
    company_accounting_required = serializers.BooleanField(
        allow_null=True, required=False
    )
    environment = serializers.CharField()
    emission_type = serializers.CharField()


class InvoicePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoicePayment
        exclude = ("invoice",)


class InvoiceLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = InvoiceLine
        exclude = ("invoice",)


class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True, read_only=True)
    payments = InvoicePaymentSerializer(many=True, read_only=True)
    sri_config = serializers.SerializerMethodField(
        source="get_sri_config", read_only=True
    )

    class Meta:
        model = Invoice
        fields = "__all__"

    @inject
    def get_sri_config(
        self,
        obj,
        site_repository: SiteRepository = Provide["core_package.site_repository"],
    ):
        sri_config = site_repository.get_sri_config()
        return SRIConfigSerializer(sri_config).data

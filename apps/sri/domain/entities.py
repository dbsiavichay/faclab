from datetime import datetime
from typing import Any, Dict, List, Optional

import pytz
from pydantic import (
    AliasChoices,
    AliasPath,
    BaseModel,
    Field,
    field_serializer,
    field_validator,
)


class TaxInfo(BaseModel):
    environment: str = Field(serialization_alias="ambiente")
    emission_type: str = Field(serialization_alias="tipoEmision")
    company_name: str = Field(serialization_alias="razonSocial")
    company_trade_name: str = Field(serialization_alias="nombreComercial")
    company_code: str = Field(serialization_alias="ruc")
    voucher_access_code: str = Field(
        validation_alias=AliasChoices("voucher_access_code", "access_code"),
        serialization_alias="claveAcceso",
    )
    voucher_type_code: str = Field(serialization_alias="codDoc")
    company_branch_code: str = Field(serialization_alias="estab")
    company_sale_point_code: str = Field(serialization_alias="ptoEmi")
    voucher_sequence: str = Field(
        validation_alias=AliasChoices("voucher_sequence", "sequence"),
        serialization_alias="secuencial",
    )
    company_main_address: str = Field(serialization_alias="dirMatriz")


class TaxValueInfo(BaseModel):
    code: int = Field(serialization_alias="codigo")
    percentage_code: int = Field(serialization_alias="codigoPorcentaje")
    fee: Optional[int] = Field(serialization_alias="tarifa", default=None)
    base: float = Field(serialization_alias="baseImponible")
    value: float = Field(serialization_alias="valor")

    @field_validator("base", "value", mode="before")
    @classmethod
    def round_two_decimals(cls, value: float) -> float:
        return round(value, 2)


class InvoiceInfo(BaseModel):
    voucher_date: datetime = Field(
        validation_alias=AliasChoices("voucher_date", "date"),
        serialization_alias="fechaEmision",
    )
    company_branch_address: str = Field(serialization_alias="dirEstablecimiento")
    # specialContributorCode: str = Field(serialization_alias="contribuyenteEspecial")
    company_accounting_required: bool = Field(
        serialization_alias="obligadoContabilidad"
    )
    customer_code_type: str = Field(
        validation_alias=AliasChoices("customer_code_type", "code_type_code"),
        serialization_alias="tipoIdentificacionComprador",
    )
    customer_bussiness_name: str = Field(
        validation_alias=AliasChoices("customer_bussiness_name", "bussiness_name"),
        serialization_alias="razonSocialComprador",
    )
    customer_code: str = Field(
        validation_alias=AliasChoices("customer_code", "code"),
        serialization_alias="identificacionComprador",
    )
    voucher_subtotal: float = Field(
        validation_alias=AliasChoices("voucher_subtotal", "subtotal"),
        serialization_alias="totalSinImpuestos",
    )
    voucher_discount: float = Field(default=0, serialization_alias="totalDescuento")
    voucher_taxes: List[TaxValueInfo] = Field(serialization_alias="totalConImpuestos")
    voucher_tip: float = Field(default=0, serialization_alias="propina")
    voucher_total: float = Field(
        validation_alias=AliasChoices("voucher_total", "total"),
        serialization_alias="importeTotal",
    )
    currency: str = Field(default="DOLAR", serialization_alias="moneda")

    @field_validator(
        "voucher_subtotal",
        "voucher_discount",
        "voucher_tip",
        "voucher_total",
        mode="before",
    )
    @classmethod
    def round_two_decimals(cls, value: float) -> float:
        return round(value, 2)

    @field_serializer("voucher_date")
    def serialize_voucher_date(self, voucher_date: datetime, _info):
        return voucher_date.strftime("%d/%m/%Y")

    @field_serializer("company_accounting_required")
    def serialize_company_accounting_required(
        self, company_accounting_required: bool, _info
    ):
        return "SI" if company_accounting_required else "NO"

    @field_serializer("voucher_taxes")
    def serialize_voucher_taxes(self, voucher_taxes: List[TaxValueInfo], _info):
        return {"totalImpuesto": voucher_taxes}


class InvoiceDetailInfo(BaseModel):
    main_code: str = Field(serialization_alias="codigoPrincipal")
    aux_code: str = Field(serialization_alias="codigoAuxiliar")
    description: str = Field(serialization_alias="descripcion")
    quantity: float = Field(serialization_alias="cantidad")
    unit_price: float = Field(serialization_alias="precioUnitario")
    discount: float = Field(default=0, serialization_alias="descuento")
    subtotal: float = Field(serialization_alias="precioTotalSinImpuesto")
    taxes: List[TaxValueInfo] = Field(serialization_alias="impuestos")

    @field_validator("quantity", "unit_price", "discount", "subtotal", mode="before")
    @classmethod
    def round_two_decimals(cls, value: float) -> float:
        return round(value, 2)

    @field_serializer("taxes")
    def serialize_taxes(self, taxes: List[TaxValueInfo], _info):
        # TODO: validar tarifa y formato
        return {"impuesto": taxes}


class PaymentInfo(BaseModel):
    type: str = Field(serialization_alias="formaPago")
    value: float = Field(
        validation_alias=AliasChoices("value", "amount"), serialization_alias="total"
    )
    deadline: int = Field(default=0, serialization_alias="plazo")
    time_unit: str = Field(default="dias", serialization_alias="unidadTiempo")

    @field_validator("value", mode="before")
    @classmethod
    def round_two_decimals(cls, value: float) -> float:
        return round(value, 2)


class Message(BaseModel):
    type: str = Field(alias="tipo")
    code: str = Field(alias="identificador")
    text: str = Field(alias="mensaje")
    additional_info: Optional[str] = Field(alias="informacionAdicional")


class VoucherResult(BaseModel):
    access_code: str = Field(validation_alias="claveAcceso")
    messages: List[Message] = Field(
        validation_alias=AliasPath("mensajes", "mensaje"), default=[]
    )

    @field_validator("messages", mode="before")
    @classmethod
    def transform_messages(cls, original_messages: List[Any]) -> Dict[str, Any]:
        messages = [dict(om.__dict__["__values__"]) for om in original_messages]
        return messages


class VoucherResponse(BaseModel):
    status: str = Field(validation_alias="estado")
    results: List[VoucherResult] = Field(
        validation_alias=AliasPath("comprobantes", "comprobante"), default=[]
    )

    @field_validator("results", mode="before")
    @classmethod
    def transform_results(cls, original_results: List[Any]) -> Dict[str, Any]:
        results = [dict(ov.__dict__["__values__"]) for ov in original_results]
        return results


class AuthorizationResult(BaseModel):
    environment: str = Field(alias="ambiente")
    status: str = Field(alias="estado")
    authorization_date: Optional[datetime] = Field(alias="fechaAutorizacion")
    authorization_number: Optional[str] = Field(alias="numeroAutorizacion")
    voucher: str = Field(alias="comprobante")
    messages: List[Message] = Field(
        validation_alias=AliasPath("mensajes", "mensaje"), default=[]
    )

    @field_validator("authorization_date", mode="before")
    @classmethod
    def transform_authorization_date(cls, original_date: datetime) -> datetime:
        return original_date.astimezone(pytz.utc)

    @field_validator("messages", mode="before")
    @classmethod
    def transform_messages(cls, original_messages: List[Any]) -> Dict[str, Any]:
        messages = [dict(om.__dict__["__values__"]) for om in original_messages]
        return messages


class AuthorizationResponse(BaseModel):
    access_code: str = Field(alias="claveAccesoConsultada")
    results_count: int = Field(alias="numeroComprobantes")
    results: List[AuthorizationResult] = Field(
        validation_alias=AliasPath("autorizaciones", "autorizacion"), default=[]
    )

    @field_validator("results", mode="before")
    @classmethod
    def transform_results(cls, original_results: List[Any]) -> Dict[str, Any]:
        results = [dict(ov.__dict__["__values__"]) for ov in original_results]
        return results

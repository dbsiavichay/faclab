from datetime import datetime
from typing import Any, Dict, List, Optional

import pytz
from pydantic import AliasPath, BaseModel, Field, field_validator


class VoucherEntity(BaseModel):
    code: str
    file: bytes
    authorization_date: Optional[datetime]


class VoucherAPIMessage(BaseModel):
    type: str = Field(alias="tipo")
    code: str = Field(alias="identificador")
    text: str = Field(alias="mensaje")
    additional_info: Optional[str] = Field(alias="informacionAdicional")


class VoucherAPI(BaseModel):
    environment: str = Field(alias="ambiente")
    status: str = Field(alias="estado")
    authorization_date: Optional[datetime] = Field(alias="fechaAutorizacion")
    authorization_number: Optional[str] = Field(alias="numeroAutorizacion")
    voucher_xml: str = Field(alias="comprobante")
    messages: List[VoucherAPIMessage] = Field(
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


class VoucherAPIResponse(BaseModel):
    queried_code: str = Field(alias="claveAccesoConsultada")
    vouchers_count: int = Field(alias="numeroComprobantes")
    vouchers: List[VoucherAPI] = Field(
        validation_alias=AliasPath("autorizaciones", "autorizacion"), default=[]
    )

    @field_validator("vouchers", mode="before")
    @classmethod
    def transform_vouchers(cls, original_vouchers: List[Any]) -> Dict[str, Any]:
        vouchers = [dict(ov.__dict__["__values__"]) for ov in original_vouchers]
        return vouchers

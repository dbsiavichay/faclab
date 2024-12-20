from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from .enums import PaymentTypeEnum, VoucherStatusEnum


class CustomerEntity(BaseModel):
    id: int
    code: str
    first_name: Optional[str]
    last_name: Optional[str]
    bussiness_name: str
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    code_type_code: str


class VoucherTypeEntity(BaseModel):
    id: int = Field(gt=0)
    code: str
    name: str
    current: int = Field(ge=0)
    ends: int = Field(ge=0)


class InvoiceLineEntity(BaseModel):
    quantity: float
    unit_price: float
    subtotal: Optional[float] = 0
    tax: Optional[float] = 0
    total: Optional[float] = 0
    product_id: int
    invoice_id: int


class InvoicePaymentEntity(BaseModel):
    type: PaymentTypeEnum
    amount: float
    invoice_id: int


class InvoiceEntity(BaseModel):
    id: Optional[int] = Field(gt=0)
    date: Optional[datetime]
    authorization_date: Optional[datetime]
    voucher_type_code: str
    access_code: Optional[str]
    company_branch_code: str = Field(max_length=3)
    company_sale_point_code: str = Field(max_length=3)
    sequence: str = Field(max_length=9)
    subtotal: float
    tax: float
    total: float
    status: VoucherStatusEnum = Field(default=VoucherStatusEnum.GENERATED)
    xml_bytes: Optional[bytes] = None
    xml_str: Optional[str] = None
    errors: dict
    customer_id: int = None
    customer: CustomerEntity = None
    lines: List[InvoiceLineEntity] = []
    payments: List[InvoicePaymentEntity] = []

    @field_validator("total", mode="before")
    @classmethod
    def round_two_decimals(cls, value: float) -> float:
        return round(value, 2)

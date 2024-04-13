from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, FileUrl


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


class InvoiceEntity(BaseModel):
    id: Optional[int] = Field(gt=0)
    issue_date: Optional[datetime]
    authorization_date: Optional[datetime]
    code: Optional[str]
    company_branch_code: str = Field(max_length=3)
    company_sale_point_code: str = Field(max_length=3)
    sequence: str = Field(max_length=9)
    subtotal: float
    tax: float
    total: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(max_length=4)  # TODO: agregar choices
    file_url: Optional[FileUrl] = None
    errors: dict
    customer: CustomerEntity = None
    lines: List[InvoiceLineEntity] = []

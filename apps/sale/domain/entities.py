from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, FileUrl


class VoucherTypeEntity(BaseModel):
    id: int = Field(gt=0)
    code: str
    name: str
    current: int = Field(ge=0)
    ends: int = Field(ge=0)


class InvoiceEntity(BaseModel):
    id: Optional[int] = Field(gt=0)
    issue_date: Optional[datetime]
    authorization_date: Optional[datetime]
    code: Optional[str]
    company_code: str = Field(max_length=3)
    company_point_sale_code: str = Field(max_length=3)
    sequence: str = Field(max_length=9)
    subtotal: float
    tax: float
    total: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(max_length=4)  # TODO: agregar choices
    file: Optional[FileUrl]
    errors: dict

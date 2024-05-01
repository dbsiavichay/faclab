from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PurchaseLineEntity(BaseModel):
    id: Optional[int]
    quantity: float
    unit_price: float
    subtotal: Optional[float] = 0
    tax: Optional[float] = 0
    total: Optional[float] = 0
    product_id: int
    invoice_id: int


class PurchaseEntity(BaseModel):
    id: int
    date: datetime
    invoice_number: str
    subtotal: Optional[float] = 0
    tax: Optional[float] = 0
    total: Optional[float] = 0
    provider_id: int
    lines: List[PurchaseLineEntity] = []

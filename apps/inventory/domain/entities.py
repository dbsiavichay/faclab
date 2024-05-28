from typing import Optional

from pydantic import BaseModel

from .enums import StockMoveTypeEnum


class StockMove(BaseModel):
    type: StockMoveTypeEnum
    entry: float = 0
    outflow: float = 0
    stock: float = 0
    product_id: int


class Product(BaseModel):
    id: int
    code: str
    sku: Optional[str]
    name: str
    short_name: str
    description: Optional[str]
    stock: float = 0

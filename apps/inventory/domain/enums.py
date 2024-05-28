from enum import Enum


class StockMoveTypeEnum(str, Enum):
    INITIAL = "i"
    PURCHASE = "p"
    SALE = "s"

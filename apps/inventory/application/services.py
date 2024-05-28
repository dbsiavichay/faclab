from typing import List, Tuple

from apps.inventory.domain.entities import Product
from apps.inventory.domain.enums import StockMoveTypeEnum

from .usecases import CreateEntryStockMoveUseCase


class InventoryService:
    def __init__(
        self, create_entry_stock_move_usecase: CreateEntryStockMoveUseCase
    ) -> None:
        self.create_entry_stock_move_usecase = create_entry_stock_move_usecase

    def create_purchase_stock_move(self, moves: List[Tuple[float, Product]]):
        self.create_entry_stock_move_usecase.execute(StockMoveTypeEnum.PURCHASE, moves)

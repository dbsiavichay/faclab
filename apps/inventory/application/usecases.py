from typing import List, Tuple

from apps.inventory.domain.choices import StockMoveType
from apps.inventory.domain.entities import Product, StockMove
from apps.inventory.domain.repositories import ProductRepository, StockMoveRepository


class CreateEntryStockMoveUseCase:
    def __init__(
        self,
        stock_move_repository: StockMoveRepository,
        product_repository: ProductRepository,
    ) -> None:
        self.stock_move_repository = stock_move_repository
        self.product_repository = product_repository

    def execute(self, type: StockMoveType, moves: List[Tuple[float, Product]]):
        stock_moves = []

        for quantity, product in moves:
            new_stock = product.stock + quantity
            product.stock = new_stock
            stock_moves.append(
                StockMove(
                    type=type, entry=quantity, stock=new_stock, product_id=product.id
                )
            )

        self.stock_move_repository.bulk_create(stock_moves)
        products = [product for _, product in moves]
        self.product_repository.bulk_update(products, update_fiels=["stock"])

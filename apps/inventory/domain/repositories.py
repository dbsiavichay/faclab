from abc import ABC, abstractmethod
from typing import List

from .entities import Product, StockMove


class StockMoveRepository(ABC):
    @abstractmethod
    def bulk_create(self, stock_moves: List[StockMove]):
        pass


class ProductRepository(ABC):
    @abstractmethod
    def bulk_update(self, products: List[Product], update_fiels: List[str] = None):
        pass

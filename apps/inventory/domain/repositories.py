from abc import ABC, abstractmethod
from typing import List

from .entities import StockMove


class StockMoveRepository(ABC):
    @abstractmethod
    def bulk_create(self, stock_moves: List[StockMove]):
        pass

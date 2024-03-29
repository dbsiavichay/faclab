from abc import ABC, abstractmethod
from typing import List

from simple_menu import MenuItem


class MenuRepository(ABC):
    @abstractmethod
    def retrieve_menu_item(self) -> MenuItem:
        pass

    @abstractmethod
    def retrieve_menu_items(self) -> List[MenuItem]:
        pass

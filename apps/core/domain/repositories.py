from abc import ABC, abstractmethod
from typing import List

from simple_menu import MenuItem

from .entities import SRIConfig


class MenuRepository(ABC):
    @abstractmethod
    def retrieve_menu_item(self) -> MenuItem:
        pass

    @abstractmethod
    def retrieve_menu_items(self) -> List[MenuItem]:
        pass


class SiteRepository(ABC):
    @abstractmethod
    def get_sri_config(self) -> SRIConfig:
        pass

    @abstractmethod
    def refresh_site(self) -> None:
        pass

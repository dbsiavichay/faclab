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
    def get_current_site(self):
        pass

    @abstractmethod
    def get_site_id(self) -> int:
        pass

    @abstractmethod
    def get_sri_config(self) -> SRIConfig:
        pass

    @abstractmethod
    def delete_sri_cache_config(self) -> None:
        pass

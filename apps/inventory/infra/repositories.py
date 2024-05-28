from typing import List

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from apps.core.domain.repositories import MenuRepository
from apps.inventory.domain.entities import Product, StockMove
from apps.inventory.domain.repositories import ProductRepository, StockMoveRepository

from .models import Product as DjangoProduct
from .models import StockMove as DjangoStockMove


class MenuRepositoryImpl(MenuRepository):
    def retrieve_menu_item(self) -> MenuItem:
        submenu_items = self.retrieve_menu_items()

        return MenuItem(
            _("inventory").capitalize(), "#", icon="bxs-store", children=submenu_items
        )

    def retrieve_menu_items(self) -> List[MenuItem]:
        return [
            MenuItem(
                _("categories").capitalize(),
                reverse("packs:inventory_productcategory_list"),
                weight=11,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("measures").capitalize(),
                reverse("packs:inventory_measure_list"),
                weight=12,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("products").capitalize(),
                reverse("packs:inventory_product_list"),
                weight=13,
                icon="bx-right-arrow-alt",
            ),
            MenuItem(
                _("operations").capitalize(),
                "#",
                weight=14,
                icon="bx-right-arrow-alt",
                children=[
                    MenuItem(
                        _("inventory adjustment").capitalize(),
                        reverse("packs:inventory_stockmove_list"),
                        weight=1,
                        icon="bx-right-arrow-alt",
                    ),
                ],
            ),
        ]


class StockMoveRepositoryImpl(StockMoveRepository):
    def bulk_create(self, stock_moves: List[StockMove]):
        django_stock_moves = [
            DjangoStockMove(**stock_move.model_dump()) for stock_move in stock_moves
        ]
        DjangoStockMove.objects.bulk_create(django_stock_moves)


class ProductRepositoryImpl(ProductRepository):
    def bulk_update(self, products: List[Product], update_fiels: List[str] = None):
        django_products = [
            DjangoProduct(**product.model_dump()) for product in products
        ]
        DjangoProduct.objects.bulk_update(django_products, update_fiels)

from django.db.models import OuterRef, Subquery

from apps.inventory.domain.choices import PriceType
from apps.inventory.infra.models import Product, ProductPrice


class ProductQueryset:
    subquery_first_price = ProductPrice.objects.filter(
        product=OuterRef("pk"), type=PriceType.SALE
    ).values("amount")
    product_with_first_price = Product.objects.annotate(
        first_price=Subquery(subquery_first_price[:1])
    ).all()
    subquery_cost_price = ProductPrice.objects.filter(
        product=OuterRef("pk"), type=PriceType.PURCHASE
    ).values("amount")
    product_with_first_cost_price = Product.objects.annotate(
        first_cost_price=Subquery(subquery_cost_price[:1])
    ).all()

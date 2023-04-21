from django.db.models import OuterRef, Subquery

from apps.warehouses.enums import PriceTypes
from apps.warehouses.models import Price, Product


class ProductQueryset:
    subquery_first_price = Price.objects.filter(
        product=OuterRef("pk"), type=PriceTypes.SALE
    ).values("amount")
    product_with_first_price = Product.objects.annotate(
        first_price=Subquery(subquery_first_price[:1])
    ).all()

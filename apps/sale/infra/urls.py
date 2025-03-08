from rest_framework.routers import DefaultRouter

from .viewsets import InvoiceViewSet

router = DefaultRouter()
router.register(r"invoice", InvoiceViewSet, basename="invoice")

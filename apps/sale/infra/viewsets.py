from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            invoice = Invoice.objects.get(pk=pk)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND
            )

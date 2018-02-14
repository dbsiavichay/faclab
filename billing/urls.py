from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
	path('customer/', CustomerListView.as_view(), name='customers'),    
	path('customer/add/', CustomerCreateView.as_view(), name='add_customer'),    
	path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='update_customer'),    	
	path('tax/', TaxListView.as_view(), name='taxes'),    
	path('tax/add/', TaxCreateView.as_view(), name='add_tax'),    	
	path('tax/<int:pk>/update/', TaxUpdateView.as_view(), name='update_tax'),
	path('tax/<int:pk>/', TaxDetailView.as_view(), name='detail_tax'),    	
	path('invoice/', InvoiceListView.as_view(), name='invoices'),    
	path('invoice/add/', InvoiceCreateView.as_view(), name='add_invoice'),
	path('invoice/<int:pk>/update/', InvoiceUpdateView.as_view(), name='update_invoice'),
	path('invoice/<int:pk>/invoiced/', InvoiceInvoicedView.as_view(), name='invoiced_invoice'),
]
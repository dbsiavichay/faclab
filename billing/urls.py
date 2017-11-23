from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^customer/$', CustomerListView.as_view(), name='customers'),    
	url(r'^customer/add/$', CustomerCreateView.as_view(), name='add_customer'),    
	url(r'^tax/$', TaxListView.as_view(), name='taxes'),    
	url(r'^tax/add/$', TaxCreateView.as_view(), name='add_tax'),    	
	url(r'^tax/(?P<pk>\d+)/$', TaxDetailView.as_view(), name='detail_tax'),    	
	url(r'^invoice/$', InvoiceListView.as_view(), name='invoices'),    
	url(r'^invoice/add/$', InvoiceCreateView.as_view(), name='add_invoice'),    	
]
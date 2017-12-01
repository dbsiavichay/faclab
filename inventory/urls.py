from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^werehouse/$', WerehouseListView.as_view(), name='werehouses'),    
	url(r'^werehouse/add/$', WerehouseCreateView.as_view(), name='add_werehouse'),
	url(r'^werehouse/(?P<pk>\d+)/update/$', WerehouseUpdateView.as_view(), name='update_werehouse'),    
	url(r'^category/$', CategoryListView.as_view(), name='categories'),    
	url(r'^category/add/$', CategoryCreateView.as_view(), name='add_category'),    
	url(r'^category/(?P<pk>\d+)/update/$', CategoryUpdateView.as_view(), name='update_category'),    
	url(r'^product/$', ProductListView.as_view(), name='products'),    
	url(r'^product/add/$', ProductCreateView.as_view(), name='add_product'),    
	url(r'^product/(?P<pk>\d+)/update/$', ProductUpdateView.as_view(), name='update_product'),    
	url(r'^product/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail_product'),    
]
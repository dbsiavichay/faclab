from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^category/$', CategoryListView.as_view(), name='categories'),    
	url(r'^category/add/$', CategoryCreateView.as_view(), name='add_category'),    
	url(r'^product/$', ProductListView.as_view(), name='products'),    
	url(r'^product/add/$', ProductCreateView.as_view(), name='add_product'),    
]
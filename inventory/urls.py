from django.urls import path
from .views import *

urlpatterns = [
	path('werehouse/', WerehouseListView.as_view(), name='werehouses'),    
	path('werehouse/add/', WerehouseCreateView.as_view(), name='add_werehouse'),
	path('werehouse/<int:pk>/update/', WerehouseUpdateView.as_view(), name='update_werehouse'),    
	path('category/', CategoryListView.as_view(), name='categories'),    
	path('category/add/', CategoryCreateView.as_view(), name='add_category'),    
	path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='update_category'),    
	path('product/', ProductListView.as_view(), name='products'),    
	path('product/add/', ProductCreateView.as_view(), name='add_product'),    
	path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),    
	path('product/<int:pk>/', ProductDetailView.as_view(), name='detail_product'),    
]
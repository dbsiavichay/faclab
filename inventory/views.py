# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import *		

class WerehouseListView(ListView):
	model = Werehouse
	paginate_by = 10

class WerehouseCreateView(CreateView):
	model = Werehouse
	fields = '__all__'
	success_url = reverse_lazy('werehouses')

class WerehouseUpdateView(UpdateView):
	model = Werehouse
	fields = '__all__'
	success_url = reverse_lazy('werehouses')

class CategoryListView(ListView):
	model = Category
	paginate_by = 10

class CategoryCreateView(CreateView):
	model = Category
	fields = '__all__'
	success_url = reverse_lazy('categories')

class CategoryUpdateView(UpdateView):
	model = Category
	fields = '__all__'
	success_url = reverse_lazy('categories')

class ProductListView(ListView):
	model = Product
	paginate_by = 10

class ProductCreateView(CreateView):
	model = Product
	fields = '__all__'
	success_url = reverse_lazy('products')

class ProductUpdateView(UpdateView):
	model = Product
	fields = '__all__'
	success_url = reverse_lazy('products')

class ProductDetailView(DetailView):
	model = Product

	def get(self, request, *args, **kwargs):
		from django.forms.models import model_to_dict

		if not request.is_ajax():
			return super(ProductDetailView, self).get(request, *args, **kwargs)
		self.object = self.get_object()
		obj_dict = model_to_dict(self.object)
		return JsonResponse(obj_dict)
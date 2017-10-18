# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from .models import *		

class CategoryListView(ListView):
	model = Category

class CategoryCreateView(CreateView):
	model = Category
	fields = '__all__'
	success_url = reverse_lazy('categories')

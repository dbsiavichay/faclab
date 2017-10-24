# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import *

class CustomerListView(ListView):
	model = Customer

class CustomerCreateView(CreateView):
	model = Customer
	fields = '__all__'
	success_url = reverse_lazy('customers')

class TaxListView(ListView):
	model = Tax

class TaxCreateView(CreateView):
	model = Tax
	fields = '__all__'
	success_url = reverse_lazy('taxes')
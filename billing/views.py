# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import *
from .models import *

class CustomerListView(ListView):
	model = Customer

class CustomerCreateView(CreateView):
	model = Customer
	fields = '__all__'
	success_url = reverse_lazy('customers')

class CustomerUpdateView(UpdateView):
	model = Customer
	fields = '__all__'
	success_url = reverse_lazy('customers')

class TaxListView(ListView):
	model = Tax

class TaxCreateView(CreateView):
	model = Tax
	fields = '__all__'
	success_url = reverse_lazy('taxes')

class TaxUpdateView(UpdateView):
	model = Tax
	fields = '__all__'
	success_url = reverse_lazy('taxes')

class TaxDetailView(DetailView):
	model = Tax

	def get(self, request, *args, **kwargs):
		from django.forms.models import model_to_dict

		if not request.is_ajax():
			return super(TaxDetailView, self).get(request, *args, **kwargs)
		self.object = self.get_object()
		obj_dict = model_to_dict(self.object)
		return JsonResponse(obj_dict)

class InvoiceListView(ListView):
	model = Invoice
	paginate_by = 10

class InvoiceCreateView(CreateView)	:
	model = Invoice
	form_class = InvoiceForm
	success_url = reverse_lazy('invoices')

	def get_context_data(self, **kwargs):
		context = super(InvoiceCreateView, self).get_context_data(**kwargs)
		context['invoiceline_formset'] = self.get_invoiceline_formset()

		return context

	def form_valid(self, form):
		invoiceline_formset = self.get_invoiceline_formset()
		
		if invoiceline_formset.is_valid():
			self.object = form.save(commit=False)
			invoiceline_formset.instance = self.object
			invoiceline_formset.save(commit=False)			
			self.object.save()
			invoiceline_formset.save()
			return redirect(self.get_success_url())
		else:
			return self.form_invalid(form)

	def get_invoiceline_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None
		formset = InvoiceLineInlineFormSet(post_data)
		return formset
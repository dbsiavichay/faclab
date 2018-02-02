# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Customer(models.Model):
	name = models.CharField(max_length=140, verbose_name='nombre')
	ruc = models.CharField(max_length=16, verbose_name='ruc')
	telephone = models.CharField(max_length=10, verbose_name='teléfono')
	address = models.CharField(max_length=100, verbose_name='dirección')
	email = models.EmailField(blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse_lazy('update_customer', args=[self.id])

class Tax(models.Model):
	SCOPE_CHOICES = ((1, 'Ventas'),(2, 'Compras'),(3, 'Ninguno'))

	AMOUNT_TYPE_FIXED = 1
	AMOUNT_TYPE_PERCENT = 2
	AMOUNT_TYPE_CHOICES = ((AMOUNT_TYPE_FIXED, 'Fijo'),(AMOUNT_TYPE_PERCENT, 'Porcentaje sobre el precio'))

	name = models.CharField(max_length=140, verbose_name='nombre')
	scope = models.PositiveSmallIntegerField(choices=SCOPE_CHOICES, verbose_name='ámbito')
	amount_type = models.PositiveSmallIntegerField(choices=AMOUNT_TYPE_CHOICES, verbose_name='tipo de cálculo')
	amount = models.FloatField(verbose_name='valor')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse_lazy('update_tax', args=[self.id])

	def get_scope(self):
		return dict(self.SCOPE_CHOICES).get(self.scope)

	def get_amount_type(self):
		return dict(self.AMOUNT_TYPE_CHOICES).get(self.amount_type)
		

class Invoice(models.Model):	
	DRAFT = 1
	INVOICED = 2
	ISSUED = 3
	PAID = 4
	ANNULLED = 10		

	STATUS_CHOICES = (
		(DRAFT, 'Borrador'),(INVOICED, 'Facturado'),(ISSUED, 'Emitido'),
		(PAID, 'Pagado'),(ANNULLED, 'Anulado'),
	)

	STATUS_LABELS = (
		(DRAFT, 'default'),(INVOICED, 'primary'),(ISSUED, 'success'),
		(PAID, 'info'),(ANNULLED, 'danger'),
	)

	untaxed_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='base imponible')
	tax_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='impuestos')
	total_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='total')
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DRAFT)
	date = models.DateField(verbose_name='fecha de emisión')
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='cliente')

	def get_status(self):
		return format_html(
            '<span class="label label-{}">{}</span>',
            dict(self.STATUS_LABELS).get(self.status),            
            dict(self.STATUS_CHOICES).get(self.status),
        )
	
	def get_absolute_url(self):
		return reverse_lazy('update_invoice', args=[self.id])

class InvoiceLine(models.Model):
	quantity = models.FloatField(validators = [MinValueValidator(0.01),])	
	unit_price = models.DecimalField(
		max_digits=9, decimal_places=2, verbose_name='precio unitario',
		validators = [MinValueValidator(0.01),]
	)
	total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='subtotal')
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)
	taxes = models.ManyToManyField(Tax)
	product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

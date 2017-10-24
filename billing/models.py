# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Customer(models.Model):
	name = models.CharField(max_length=140, verbose_name='nombre')
	ruc = models.CharField(max_length=16, verbose_name='ruc')
	telephone = models.CharField(max_length=10, verbose_name='teléfono')
	address = models.CharField(max_length=100, verbose_name='dirección')
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)

class Tax(models.Model):
	SCOPE_CHOICES = ((1, 'Ventas'),(2, 'Compras'),(3, 'Ninguno'))
	AMOUNT_TYPE_CHOICES = ((1, 'Fijo'),(2, 'Porcentaje sobre el precio'))

	name = models.CharField(max_length=140, verbose_name='nombre')
	scope = models.PositiveSmallIntegerField(choices=SCOPE_CHOICES, verbose_name='ámbito')
	amount_type = models.PositiveSmallIntegerField(choices=AMOUNT_TYPE_CHOICES, verbose_name='tipo de cálculo')
	amount = models.FloatField(verbose_name='valor')

class Invoice(models.Model):
	untaxed_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='subtotal')
	tax_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='impuestos')
	total_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='total')
	#status = models.PositiveSmallIntegerField()
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)
	customer = models.ForeignKey(Customer)	

class InvoiceLine(models.Model):
	quantity = models.FloatField()
	unit_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='total')
	total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='total')
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)
	taxes = models.ManyToManyField(Tax)
	product = models.ForeignKey('inventory.Product')

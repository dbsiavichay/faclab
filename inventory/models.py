# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Werehouse(models.Model):
	name = models.CharField(max_length=140)
	address = models.CharField(max_length=140)	

class Category(models.Model):
	name = models.CharField(max_length=140)
	create_date = models.DateTimeField(auto_now_add=True)
	parent = models.ForeignKey('self')	

class Product(models.Model):
	TYPE_CHOICES = (
		(1, 'Producto'),
		(2, 'Servicio')		
	)

	name = models.CharField(max_length=140)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	warranty = models.FloatField()
	type_of_product = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)
	category = models.ForeignKey(Category)
	werehouse = models.ForeignKey(Werehouse)	

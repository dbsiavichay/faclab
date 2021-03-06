# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse_lazy

class Werehouse(models.Model):
	name = models.CharField(max_length=140, verbose_name='nombre')
	address = models.CharField(max_length=140, verbose_name='dirección')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse_lazy('update_werehouse', args=[self.id])


class Category(models.Model):
	name = models.CharField(max_length=140, verbose_name='nombre')
	create_date = models.DateTimeField(auto_now_add=True)
	parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, verbose_name='padre')

	def __str__(self):		
		return '%s / %s' % (str(self.parent),self.name) if self.parent else self.name

	def get_absolute_url(self):
		return reverse_lazy('update_category', args=[self.id])

class Product(models.Model):
	TYPE_CHOICES = (
		(1, 'Producto'),
		(2, 'Servicio')		
	)

	name = models.CharField(max_length=140, verbose_name='nombre')
	price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='precio')
	warranty = models.FloatField(blank=True, null=True, verbose_name='garantía')
	type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, verbose_name='tipo')
	create_date = models.DateTimeField(auto_now_add=True)
	write_date = models.DateTimeField(auto_now=True)
	category = models.ForeignKey(Category, verbose_name='categoría', on_delete=models.CASCADE)
	werehouse = models.ForeignKey(Werehouse, blank=True, null=True, on_delete=models.CASCADE, verbose_name='bodega')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse_lazy('update_product', args=[self.id])

from django.db import models

from .enums import CodeTypes


class Customer(models.Model):
    code_type = models.CharField(choices=CodeTypes.choices, max_length=4)
    code = models.CharField(max_length=16)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    bussiness_name = models.CharField(max_length=128)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.bussiness_name

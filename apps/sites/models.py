from django.db import models


class Config(models.Model):
    sri_config = models.JSONField(default=dict)

from django.db import models

class Measurement(models.Model):
    unit_short = models.CharField(max_length=100)
    unit_long = models.CharField(max_length=100)
    unit_plural = models.CharField(max_length=100)

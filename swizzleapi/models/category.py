from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description= models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description= models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

    @property
    def can_edit(self):
        """Checking for edit authority"""
        return self.__can_edit

    @can_edit.setter
    def can_edit(self, value):
        self.__can_edit = value

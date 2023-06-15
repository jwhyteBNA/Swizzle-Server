from django.db import models

class Tag(models.Model):
    label = models.CharField(max_length=100)

    @property
    def can_edit(self):
        """Checking for edit authority"""
        return self.__can_edit

    @can_edit.setter
    def can_edit(self, value):
        self.__can_edit = value

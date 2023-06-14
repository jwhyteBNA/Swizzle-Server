from django.db import models

class Comment(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="comments")
    mixologist = models.ForeignKey("Mixologist", on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=255)
    image_url = models.TextField(null=True, blank=True)
    created_on = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=True)

    @property
    def can_edit(self):
        """Checking for edit authority"""
        return self.__can_edit

    @can_edit.setter
    def can_edit(self, value):
        self.__can_edit = value

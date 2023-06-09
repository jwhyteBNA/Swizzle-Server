from django.db import models

class Comment(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="comments")
    mixologist = models.ForeignKey("Mixologist", on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=255)
    image_url = models.TextField(null=True, blank=True)
    created_on = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=True)

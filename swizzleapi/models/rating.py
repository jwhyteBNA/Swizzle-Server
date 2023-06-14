from django.db import models

class Rating(models.Model):
    mixologist = models.ForeignKey("Mixologist", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    score = models.IntegerField()
    review = models.TextField(null=True, blank=True)

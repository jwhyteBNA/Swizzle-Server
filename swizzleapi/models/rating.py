from django.db import models
from django.core.validators import MaxValueValidator

class Rating(models.Model):
    mixologist = models.ForeignKey("Mixologist", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MaxValueValidator(5)], null=True)

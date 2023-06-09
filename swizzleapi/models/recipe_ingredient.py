from fractions import Fraction
from django.db import models

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    measurement = models.ForeignKey("Measurement", on_delete=models.CASCADE)
    measured_amount = models.CharField(max_length=20)

    @property
    def measured_amount_fraction(self):
        """To parse both fractions and decimals"""
        try:
            decimal_value = float(self.measured_amount)
            fraction_value = Fraction(decimal_value).limit_denominator()
            return str(fraction_value)
        except ValueError:
            try:
                fraction_value = Fraction(self.measured_amount).limit_denominator()
                return str(fraction_value)
            except ValueError:
                return None

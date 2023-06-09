from django.db import models

class Favorite(models.Model):
    mixologist = models.ForeignKey(
        "Mixologist", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe.name} liked by {self.mixologist.get_full_name()}'

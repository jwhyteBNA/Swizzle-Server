from django.db import models

class Favorite(models.Model):
    mixologist = models.ForeignKey(
        "Mixologist", on_delete=models.CASCADE, related_name="user_favorite_recipes")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="user_favorite_recipes")

    def __str__(self):
        return f'{self.recipe.name} liked by {self.mixologist.get_full_name()}'

from django.db import models

class RecipeTag(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="recipe_tags")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_tags")

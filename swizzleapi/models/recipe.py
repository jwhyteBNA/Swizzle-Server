from django.db import models

class Recipe(models.Model):
    mixologist = models.ForeignKey("Mixologist", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    publication_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    image_url = models.TextField()
    ingredients = models.ManyToManyField("Ingredient", through= "RecipeIngredient", related_name= 'recipes')
    directions = models.TextField()
    notes = models.TextField(null=True)
    serving = models.IntegerField(default=1)
    approved = models.BooleanField(default=False)
    tag = models.ManyToManyField("Tag", through="RecipeTag", related_name="tagged_recipes")

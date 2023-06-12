from django.db import models


class Recipe(models.Model):
    mixologist = models.ForeignKey("Mixologist", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    publication_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    image_url = models.TextField()
    directions = models.TextField()
    notes = models.TextField(null=True)
    serving = models.IntegerField(default=1)
    approved = models.BooleanField(default=False)
    tag = models.ManyToManyField("Tag", through="RecipeTag", related_name="tagged_recipes")

    @property
    def ingredients_used(self):
        """Grab ingredients from bridge table"""
        recipe_ingredients = self.ingredients.all()
        ingredients = []
        for recipe_ingredient in recipe_ingredients:
            ingredient = {
                "measurement": {
                    "id": recipe_ingredient.measurement.id,
                    "name": recipe_ingredient.measurement.unit_short
                },
                "ingredient": {
                    "id": recipe_ingredient.ingredient.id,
                    "name": recipe_ingredient.ingredient.name
                },
                "measured_amount": recipe_ingredient.measured_amount
                
            }
            ingredients.append(ingredient)
        return ingredients

    # {
    #     ingredients: [
    #         {
    #             measurement: {
    #                 id: 4,
    #                 name: "Cups"
    #             },
    #             ingredient: {
    #                 id: 17,
    #                 name: "Carrots"
    #             },
    #             measured_amount: 9
    #         }
    #     ]
    # }
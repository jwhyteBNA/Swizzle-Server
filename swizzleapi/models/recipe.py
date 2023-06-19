from django.db import models

class Recipe(models.Model):
    mixologist = models.ForeignKey("Mixologist", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    publication_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    image_url = models.TextField(blank=True)
    ingredients = models.TextField(max_length=1500)
    directions = models.TextField()
    notes = models.TextField(null=True, blank=True)
    servings = models.IntegerField(default=1)
    original_link = models.CharField(max_length=1000, blank=True)
    approved = models.BooleanField(default=False)
    tag = models.ManyToManyField("Tag", through="RecipeTag", related_name="tagged_recipes")
    ratings = models.ManyToManyField("Mixologist", through = 'Rating', related_name='recipes_rated')
    favorites = models.ManyToManyField("Mixologist", through='Favorite', related_name='recipes')

    @property
    def can_edit(self):
        """Checking for edit authority"""
        return self.__can_edit

    @can_edit.setter
    def can_edit(self, value):
        self.__can_edit = value

    @property
    def is_favorite(self):
        """Create favorite property from logic"""
        return self.__is_favorite

    @is_favorite.setter
    def is_favorite(self, value):
        self.__is_favorite = value

    @property
    def user_rating(self):
        """Create user_rating property from logic"""
        return self.__user_rating

    @user_rating.setter
    def user_rating(self, value):
        self.__user_rating = value

    @property
    def avg_rating(self):
        """Create avg_rating property from logic"""
        return self.__avg_rating

    @avg_rating.setter
    def avg_rating(self, value):
        self.__avg_rating = value

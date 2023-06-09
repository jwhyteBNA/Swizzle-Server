# from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from swizzleapi.models import Recipe, Mixologist, Category, Tag

class RecipeView(ViewSet):

    def retrieve(self, request, pk):
        """GET request for single recipe"""
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all recipes"""
        user = Mixologist.objects.get(user=request.auth.user)

        if user:
            subscribed_mixologists = user.subscriptions.filter(ended_on__isnull=True).values_list('mixologist', flat=True)
            recipes = Recipe.objects.filter(user__id__in=subscribed_mixologists )

            mixologist = request.query_params.get('mixologist', None)
            if mixologist is not None:
                recipes = recipes.filter(user_id=mixologist)

            category = request.query_params.get('category', None)
            if category is not None:
                recipes = recipes.filter(category_id=category)

            tag = request.query_params.get('tag', None)
            if tag is not None:
                tag_array = [int(t) for t in tag.split(',')]
                for tag_id in tag_array:
                    recipes = recipes.filter(tag=tag_id)

            search = request.query_params.get('search', None)
            if search is not None:
                recipes = recipes.filter(
                    Q(name__icontains=search) |
                    Q(directions__icontains=search)|
                    Q(notes__icontains=search)
                )

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations"""
        mixologist = Mixologist.objects.get(user=request.auth.user)
        serializer = CreateRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_recipe = serializer.save(user=mixologist)
        saved_recipe.tag.set(request.data['tag'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a recipe"""

        recipe = Recipe.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category"])
        recipe.name = request.data["title"]
        recipe.publication_date = request.data["publication_date"]
        recipe.image_url = request.data["image_url"]
        recipe.directions = request.data["directions"]
        recipe.notes = request.data["notes"]
        recipe.serving = request.data["serving"]
        recipe.approved = request.data["approved"]
        recipe.category = category

        recipe.tag.clear()

        for tag_id in request.data['tag']:
            tag = Tag.objects.get(pk=tag_id)
            recipe.tag.add(tag)

        recipe.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete request for a recipe"""
        recipe = Recipe.objects.get(pk=pk)
        recipe.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False)
    def allrecipes(self, request):
        """Fetch all recipes regardless of subscription"""
        recipes = Recipe.objects.all()

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def myrecipes(self, request):
        """Get method for my recipes"""
        mixologist = Mixologist.objects.get(user=request.auth.user)
        recipes = Recipe.objects.filter(user=mixologist)

        try:
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response({"message": "Oops, this recipe isn't yours!"}, status=404)

class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Recipe
        fields = ('id', 'mixologist', 'category', 'name', 'publication_date', 'image_url', 'ingredients', 'directions', 'notes', 'serving', 'approved', 'tag')
        depth = 2

class CreateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'category', 'name', 'publication_date', 'image_url', 'directions', 'notes', 'serving','approved', 'tag')

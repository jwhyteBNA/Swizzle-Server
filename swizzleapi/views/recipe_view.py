# from django.http import HttpResponseServerError
from django.db.models import Q
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from swizzleapi.models import Recipe, Mixologist, Category, Tag

class RecipeView(ViewSet):

    def retrieve(self, request, pk):
        """GET request for single recipe"""
        mixologist = Mixologist.objects.get(user=request.auth.user)
        recipe = Recipe.objects.annotate(favorites_count=Count('favorites')).get(pk=pk)

        if recipe.mixologist == mixologist:
            recipe.can_edit = True
        elif mixologist.user.is_staff:
            recipe.can_edit = True
        else:
            recipe.can_edit = False

        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all recipes"""
        mixologist = Mixologist.objects.get(user=request.auth.user)
        recipes = Recipe.objects.annotate(
                favorites_count=Count('favorites'),
                is_favorite=Count('favorites',filter=Q(favorites=mixologist)
                ))

        for recipe in recipes:
            if recipe.mixologist == mixologist:
                recipe.can_edit = True
            else:
                recipe.can_edit = False

        mixologist = request.query_params.get('mixologist', None)
        if mixologist is not None:
            recipes = recipes.filter(mixologist_id=mixologist)

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
                Q(ingredients__icontains=search) |
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
        saved_recipe = serializer.save(mixologist=mixologist)
        saved_recipe.tag.set(request.data['tag'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a recipe"""

        recipe = Recipe.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category"])
        recipe.name = request.data["name"]
        recipe.publication_date = request.data["publication_date"]
        recipe.image_url = request.data["image_url"]
        recipe.original_link = request.data["original_link"]
        recipe.ingredients = request.data["ingredients"]
        recipe.directions = request.data["directions"]
        recipe.notes = request.data["notes"]
        recipe.servings = request.data["servings"]
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
    def mysubscriptions(self, request):
        """Fetch all subscription recipes"""
        mixologist = Mixologist.objects.get(user=request.auth.user)

        subscribed_mixologists = mixologist.subscriptions.filter(ended_on__isnull=True).values_list('mixologist', flat=True)
        recipes = Recipe.objects.filter(mixologist__id__in=subscribed_mixologists)

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def myrecipes(self, request):
        """Get method for my recipes"""
        mixologist = Mixologist.objects.get(user=request.auth.user)
        recipes = Recipe.objects.filter(mixologist=mixologist)

        try:
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response({"message": "Oops, this recipe isn't yours!"}, status=404)

    @action(methods=['post'], detail=True)
    def favorite(self, request, pk):
        """Post request for a user to favorite a recipe"""
        mixologist=Mixologist.objects.get(user=request.auth.user)
        recipe = Recipe.objects.get(pk=pk)
        recipe.favorites.add(mixologist)
        return Response({'message': 'Recipe is a winner!'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unfavorite(self, request, pk):
        """Delete request for a user to unfavorite a recipe"""
        mixologist=Mixologist.objects.get(user=request.auth.user)
        recipe = Recipe.objects.get(pk=pk)
        recipe.favorites.remove(mixologist)
        return Response({'message': 'Recipe unfavorited!'}, status=status.HTTP_204_NO_CONTENT)

class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'publication_date', 'image_url', 'ingredients', 'directions', 'notes', 'servings', 'approved', 'can_edit', 'original_link', 'category','tag', 'mixologist', 'favorites', 'is_favorite')
        depth = 2

class CreateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'publication_date', 'image_url', 'ingredients', 'directions', 'notes', 'servings', 'approved', 'original_link', 'category','tag')

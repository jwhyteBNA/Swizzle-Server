from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from swizzleapi.models import Ingredient, Recipe, Measurement

class IngredientView(ViewSet):

    def retrieve(self, request, pk):
        """Get a single ingredient"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data)
        except Ingredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get a list of all ingredients"""
        ingredients = Ingredient.objects.all()

        name = request.query_params.get('name', None)
        if name is not None:
            products = products.filter(name__icontains=name)

        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new ingredient for use"""
        try:
            ingredient = Ingredient.objects.create(
                name=request.data['name']
            )
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Update an ingredient"""
        ingredient = Ingredient.objects.get(pk=pk)

        ingredient.name = request.data['name']
        ingredient.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete an ingredient"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredient.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Ingredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True)
    def add_to_recipe(self, request, pk):
        """Add an ingredient to the current users drafted recipe"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            recipe, _ = Recipe.objects.get_or_create(
                user=request.auth.user)
            recipe.ingredients.add(ingredient)
            return Response({'message': 'product added'}, status=status.HTTP_201_CREATED)
        except Ingredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['delete'], detail=True)
    def remove_from_recipe(self, request, pk):
        """Remove an ingredient from a recipe"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            recipe = Recipe.objects.get(
                user=request.auth.user)
            recipe.ingredients.remove(ingredient)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except (Ingredient.DoesNotExist, Recipe.DoesNotExist) as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        depth = 1

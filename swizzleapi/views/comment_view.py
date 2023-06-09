from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from swizzleapi.models import Comment, Mixologist, Recipe

class CommentView(ViewSet):
    """Comment view"""

    def retrieve(self, request, pk=None):
        """Handle get requests for single comment"""
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET request for all comments"""
        comments = Comment.objects.all()

        recipe_id = request.query_params.get('recipe_id', None)
        if recipe_id is not None:
            comments = comments.filter(recipe_id=recipe_id)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST request for comment"""

        mixologist = Mixologist.objects.get(user=request.auth.user)
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(mixologist=mixologist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT request for update"""
        comment = Comment.objects.get(pk=pk)
        mixologist = Mixologist.objects.get(user=request.auth.user)
        comment.mixologist = mixologist
        recipe = Recipe.objects.get(pk=request.data['recipe'])
        comment.recipe = recipe
        comment.content = request.data['content']
        comment.image_url = request.data['image_url']
        comment.created_on = request.data['created_on']
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE request"""
        comment=Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'author', 'content', 'image_url','created_on')
        depth = 2

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'image_url', 'created_on')

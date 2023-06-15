from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from swizzleapi.models import Tag, Mixologist

class TagView(ViewSet):
    """Tags view"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single tag"""
        mixologist = Mixologist.objects.get(user=request.auth.user)
        tag = Tag.objects.get(pk=pk)
        if mixologist.user.is_staff:
            tag.can_edit = True
        else:
            tag.can_edit = False
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get list of tags"""
        mixologist = Mixologist.objects.get(user=request.auth.user)

        tags = Tag.objects.all()

        for tag in tags:
            if mixologist.user.is_staff:
                tag.can_edit = True
            else:
                tag.can_edit = False

        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""
        new_tag = Tag()
        new_tag.label = request.data['label']
        new_tag.save()

        serialized = TagSerializer(new_tag)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a tag"""

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a tag"""
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label', 'can_edit')

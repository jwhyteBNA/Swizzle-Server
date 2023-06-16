from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class UserView(ViewSet):
    """Users view"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all users"""
        users = User.objects.all().order_by('username')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a recipe"""

        user = User.objects.get(pk=request.auth.user)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["[last_name]"]
        user.username = request.data["[username]"]
        user.email = request.data["[email]"]

        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

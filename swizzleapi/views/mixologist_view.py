from datetime import datetime
from django.db.models import Q, Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from swizzleapi.models import Mixologist, Subscription

class MixologistView(ViewSet):
    """Mixologist view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user"""

        mixologist = Mixologist.objects.annotate(
            subscribed = Count(
                "subscribers",
                filter=Q(subscribers__follower__user=request.auth.user, subscribers__ended_on=None)
            ),
            unsubscribed = Count("subscribers",
            filter=Q(subscribers__follower__user=request.auth.user, subscribers__ended_on__isnull=False)
            )
        ).get(pk=pk)

        serializer = MixologistSerializer(mixologist)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all users"""
        mixologists = Mixologist.objects.all()
        serializer = MixologistSerializer(mixologists, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT request for update"""
        mixologist = Mixologist.objects.get(pk=pk)
        
        mixologist.bio = request.data['bio']
        mixologist.profile_image_url = request.data['profile_image_url']
        mixologist.active = request.data['active']
        mixologist.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'put'], detail=True)
    def subscribe(self, request, pk):
        """Post and Put Requests so user can subscribe to other users"""
        author = Mixologist.objects.get(pk=pk)
        subscriber = Mixologist.objects.get(pk=request.auth.user.id)
        if request.method == 'POST':
            Subscription.objects.create(author=author, follower=subscriber, ended_on = None)
            return Response({'message': 'Subscribed to author!'}, status=status.HTTP_201_CREATED)
        elif request.method =='PUT':
            update_subscription = Subscription.objects.get(author=author, follower=subscriber)
            update_subscription.ended_on = None
            update_subscription.save()
            return Response({'message': 'Resubscribed!'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def unsubscribe(self, request, pk):
        """Put request so user can unsubscribe from an author"""
        subscription = Subscription.objects.get(author=pk, follower=request.auth.user.id)
        subscription.ended_on = datetime.now()
        subscription.save()
        return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', 'put'], detail=False)
    def myprofile(self, request):
        """Get method for user profile"""
        user = Mixologist.objects.get(user=request.auth.user)
        profile = Mixologist.objects.filter(user=user)
    
        if request.method == 'GET':
            serializer = MixologistSerializer(profile, many=False)
            return Response(serializer.data)
        elif request.method =='PUT':
            update_profile = Mixologist.objects.get(user=request.auth.user)
            update_profile.bio = request.data['bio']
            update_profile.profile_image_url = request.data['profile_image_url']
            update_profile.save()
            return Response({'message': 'Update successful'}, status=status.HTTP_204_NO_CONTENT)


class MixologistSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = Mixologist
        fields = ('id', 'bio', 'created_on', 'active','subscriptions', 'subscribers', 'subscribed', 'unsubscribed', 'profile_image_url', 'user')
        depth = 2

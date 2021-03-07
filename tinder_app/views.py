import datetime
import django_filters.rest_framework

from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework import filters


from tinder_app.models import (
    User, UserGroup, Photo, Like, Dislike, Message
)
from .serializers import (
    UserSerializer, UserGroupSerializer, PhotoSerializer, LikeSerializer, DislikeSerializer, MessageSerializer
    )


class UserFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'get_by_distance' in request.query_params:
            queryset = self.get_queryset_by_distance(request)
        elif 'get_users_for_chat' in request.query_params:
            queryset = self.get_queryset_users_for_chat(request)
        else:
            queryset = User.objects.all()
        return queryset

    def get_queryset_users_for_chat(self, request):
        pk = request.user.pk
        user = get_object_or_404(User, pk=pk)
        users_for_chat = User.objects.filter(
            Q(user1_like_key=user) |
            Q(user2_like_key=user)
        ).filter(
            user1_like=True,
            user2_like=True
        )

        return users_for_chat.order_by('message__date')

    def get_queryset_by_distance(self, request):
        pk = request.user.pk
        user = get_object_or_404(User, pk=pk)
        users_by_distance = User.objects.exclude(
            Q(user1_like_key=user) |
            Q(user2_like_key=user)
        ).exclude(
            Q(user1_dislike_key=user) |
            Q(user2_dislike_key=user)
        )

        if user.distance_look != -1:
            geo_us1 = GEOSGeometry(user.cords)
            users_by_distance = [u for u in users_by_distance.all()
                                 if (user.group.allowed_distance == -1
                                     or user.group.allowed_distance >= user.distance_look) and
                                 user.distance_look >= int(geo_us1.distance(GEOSGeometry(u.cords)))]

        return users_by_distance[:10]


class UserView(viewsets.mixins.ListModelMixin,
               viewsets.mixins.RetrieveModelMixin,
               viewsets.mixins.CreateModelMixin,
               viewsets.GenericViewSet
               ):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_classes = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = UserFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(User, pk=pk)

    def perform_update(self, serializer):
        user = get_object_or_404(User, pk=self.request.user.pk)

        if user.block_disable is not None and user.block_disable <= datetime.datetime.now():
            if user.group.number_of_allowed_swipes != -1 and user.counter_swipes == user.group.number_of_allowed_swipes:
                day = datetime.datetime.now().day + 1
                block = datetime.datetime.now()
                block = block.replace(day=day)
                user.block_disable = block
                user.counter_swipes = 0
                user.save()
        elif user.block_disable is not None:
            raise ValidationError(f"user can't swipe until {user.block_disable}")

        serializer.save()


class UserGroupView(viewsets.mixins.ListModelMixin,
                    viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.CreateModelMixin,
                    viewsets.GenericViewSet
                    ):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(UserGroup, pk=pk)

class PhotoView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Photo, pk=pk)

class LikeListView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Like, pk=pk)


class DislikeListView(generics.ListAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Dislike, pk=pk)


class MessageListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Message, pk=pk)

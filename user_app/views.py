import datetime
import django_filters.rest_framework

from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from user_app.models import (
    User, UserGroup, Photo,
)
from .serializers import (
    UserSerializer, UserGroupSerializer, PhotoSerializer,
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
        users_for_chat = User.objects.exclude(
            id=user.pk
        ).filter(
            Q(user1_like_key=user.pk) |
            Q(user2_like_key=user.pk)
        ).exclude(
            Q(user1_like_key__user1_like=False) |
            Q(user1_like_key__user2_like=False)
        )

        return users_for_chat

    def get_queryset_by_distance(self, request):
        pk = request.user.pk
        user = get_object_or_404(User, pk=pk)
        users_by_distance = User.objects.exclude(
            Q(user1_like_key=user.pk) |
            Q(user2_like_key=user.pk)
        ).exclude(
            Q(user1_dislike_key=user.pk) |
            Q(user2_dislike_key=user.pk)
        ).exclude(
            id=user.pk
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
               viewsets.mixins.DestroyModelMixin,
               viewsets.mixins.UpdateModelMixin,
               viewsets.GenericViewSet
               ):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, UserFilter]

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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(UserGroup, pk=pk)


class PhotoView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Photo, pk=pk)

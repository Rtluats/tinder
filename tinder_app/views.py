import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from tinder_app.models import (
    User,
)
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'get_by_distance' in self.request.query_params:
            queryset = self.get_queryset_by_distance()
        elif 'get_users_for_chat' in self.request.query_params:
            queryset = self.get_queryset_users_for_chat()
        else:
            queryset = User.objects.all()
        return queryset

    def get_queryset_users_for_chat(self):
        pk = self.request.user.pk
        user = get_object_or_404(User, pk=pk)
        users_for_chat = User.objects.filter(
            Q(user1_like_key=user) |
            Q(user2_like_key=user)
        ).filter(
            user1_like=True, user2_like=True
        )

        return users_for_chat.order_by('message__date')

    def get_queryset_by_distance(self):
        pk = self.request.user.pk
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


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = get_object_or_404(User, pk=self.request.user.pk)

        if user.block_disable is not None and user.block_disable <= datetime.datetime.now():
            if user.group.number_of_allowed_swipes != -1 and user.counter_swipes == user.group.number_of_allowed_swipes:
                day = datetime.datetime.now().day + 1
                block = datetime.datetime.now()
                block = block.replace(day=day)
                user.block_disable = block
                user.save()
        elif user.block_disable is not None:
            raise ValidationError(f"user can't swipe until {user.block_disable}")

        serializer.save()

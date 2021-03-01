from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions

from tinder_app.models import (
    User, Like
)
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'get_by_distance' in self.request.query_params:
            queryset = self.get_queryset_by_distance()
        else:
            queryset = User.objects.all()
        return queryset

    def get_queryset_by_distance(self):
        pk = self.request.user.pk
        user = User.objects.get(pk=pk)
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
                                 if user.distance_look >= int(geo_us1.distance(GEOSGeometry(u.cords)))]

        return users_by_distance[:10]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        pass





from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions

from like_app.models import Like, Dislike
from like_app.serializers import LikeSerializer, DislikeSerializer


class LikeView(viewsets.mixins.ListModelMixin,
               viewsets.mixins.RetrieveModelMixin,
               viewsets.mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Like, pk=pk)


class DislikeView(viewsets.mixins.ListModelMixin,
                  viewsets.mixins.RetrieveModelMixin,
                  viewsets.mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Dislike, pk=pk)

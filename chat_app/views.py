from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions

from .models import Message
from .serializers import MessageSerializer


class MessageView(viewsets.mixins.ListModelMixin,
                  viewsets.mixins.RetrieveModelMixin,
                  viewsets.mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.query_params.get("pk", None)
        return get_object_or_404(Message, pk=pk)

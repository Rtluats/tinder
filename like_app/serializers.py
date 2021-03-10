from rest_framework import serializers

from .models import Like, Dislike


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user1_like_key', 'user2_like_key', 'user1_like', 'user2_like']


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['id', 'user1_dislike_key', 'user2_dislike_key']
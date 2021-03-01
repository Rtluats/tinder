from rest_framework import serializers
from.models import (
    User, UserGroup, Photo, Message, Like, Dislike
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'group', 'birth_date', 'counter_swipes', 'block_disable', 'distance_look', 'photo', 'cords',
            'last_cords_update'
        ]


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['id', 'number_of_allowed_swipes', 'group_name']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photo']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'from_user', 'to_user', 'date', 'text']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user1_like_key', 'user2_like_key', 'user1_like', 'user2_like']


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['id', 'user1_dislike_key', 'user2_dislike_key']

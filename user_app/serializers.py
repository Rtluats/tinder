from rest_framework import serializers
from.models import (
    User, UserGroup, Photo
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

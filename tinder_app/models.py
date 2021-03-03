from __future__ import unicode_literals
from django.db import models
from . import validator
from django.contrib.auth.models import AbstractBaseUser


class UserGroup(models.Model):
    number_of_allowed_swipes = models.IntegerField()
    allowed_distance = models.IntegerField()
    group_name = models.CharField(max_length=30)


class Photo(models.Model):
    photo = models.ImageField(upload_to="photos/")


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    birth_date = models.DateField(validators=[validator.validate_date])
    counter_swipes = models.IntegerField(default=0)
    block_disable = models.DateField(default=None, null=True)
    distance_look = models.IntegerField(default=-1)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    cords = models.CharField(max_length=200)
    last_cords_update = models.DateField(default=None, null=True)

    USERNAME_FIELD = "id"


class Like(models.Model):
    user1_like_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_like_key")
    user2_like_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2_like_key")
    user1_like = models.BooleanField(default=False)
    user2_like = models.BooleanField(default=False)


class Dislike(models.Model):
    user1_dislike_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_dislike_key")
    user2_dislike_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2_dislike_key")


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

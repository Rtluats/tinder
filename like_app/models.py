from django.db import models

# Create your models here.
from user_app.models import User


class Like(models.Model):
    user1_like_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_like_key")
    user2_like_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2_like_key")
    user1_like = models.BooleanField(default=False)
    user2_like = models.BooleanField(default=False)


class Dislike(models.Model):
    user1_dislike_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_dislike_key")
    user2_dislike_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2_dislike_key")

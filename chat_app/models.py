from django.db import models

# Create your models here.
from user_app.models import User


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

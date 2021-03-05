from __future__ import unicode_literals
from django.db import models
from . import validator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserGroup(models.Model):
    number_of_allowed_swipes = models.IntegerField()
    allowed_distance = models.IntegerField()
    group_name = models.CharField(max_length=30)


class Photo(models.Model):
    photo = models.ImageField(upload_to="photos/")


class UserManager(BaseUserManager):
    def create_user(self, email, name, birth_date, password):
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have name')
        if not birth_date:
            raise ValueError('User must have birth_date')
        if not password:
            raise ValueError('User must have a password')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            birth_date=birth_date,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, birth_date, password):
        user = self.create_user(
            email,
            name,
            birth_date,
            password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    birth_date = models.DateField(validators=[validator.validate_date])
    counter_swipes = models.IntegerField(default=0)
    block_disable = models.DateField(default=None, null=True, blank=True)
    distance_look = models.IntegerField(default=-1)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    cords = models.CharField(max_length=200, null=True, blank=True)
    last_cords_update = models.DateField(default=None, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name", "birth_date"]

    objects = UserManager()

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


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

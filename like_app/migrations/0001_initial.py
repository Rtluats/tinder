# Generated by Django 3.1.7 on 2021-03-10 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1_like', models.BooleanField(default=False)),
                ('user2_like', models.BooleanField(default=False)),
                ('user1_like_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_like_key', to=settings.AUTH_USER_MODEL)),
                ('user2_like_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_like_key', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1_dislike_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_dislike_key', to=settings.AUTH_USER_MODEL)),
                ('user2_dislike_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_dislike_key', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
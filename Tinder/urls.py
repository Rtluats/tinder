"""Tinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user_app.views import UserView
from chat_app.views import MessageView
from like_app.views import LikeView, DislikeView


user_list = UserView.as_view({
    'get': 'list',
    'post': 'create',
})

user_detail = UserView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

message_list = MessageView.as_view({
    'get': 'list',
    'post': 'create',
})

message_detail = MessageView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


likes_list = LikeView.as_view({
    'get': 'list',
    'post': 'create',
})

likes_detail = LikeView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

dislike_list = DislikeView.as_view({
    'get': 'list',
    'post': 'create',
})

dislike_detail = DislikeView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('users/', user_list, name='user-list'),
    path('user/<int:pk>/', user_detail, name='user-detail'),
    path('messages/', message_list, name='message-list'),
    path('message/<int:pk>/', message_detail, name='message-detail'),
    path('likes/', likes_list, name='likes-list'),
    path('like/<int:pk>/', likes_detail, name='likes-detail'),
    path('dislikes/', dislike_list, name='dislike-list'),
    path('dislike/<int:pk>/', dislike_detail, name='dislike-detail'),
]
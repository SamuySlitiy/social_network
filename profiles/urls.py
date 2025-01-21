from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('users/', views.UsersListView.as_view(), name='users'),
    path('messages/', views.messages_view, name='messages'),
    path('@<str:username>/', views.chat_view, name='chat'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user-profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='user-update'),
    path('friends/', FriendshipListView.as_view(), name='friendship-list'),
    path('friends/add/', FriendshipCreateView.as_view(), name='friendship-create'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/add/', SubscriptionCreateView.as_view(), name='subscription-create'),
    #path('messages/', PrivateMessageListView.as_view(), name='private-message-list'),
    #path('messages/send/', PrivateMessageCreateView.as_view(), name='private-message-create'),
]

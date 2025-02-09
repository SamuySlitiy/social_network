from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.UsersListView.as_view(), name='users'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user-profile'),
    path('profile/<int:pk>/edit/', UserUpdateView.as_view(), name='user-update'),

    path("chats/", ChatListView.as_view(), name="chats"),
    path("chat/<int:receiver_id>/", MessageListView.as_view(), name="chat"),
    path("chat/<int:receiver_id>/send/", MessageCreateView.as_view(), name="message-send"),
    path("chat/<int:receiver_id>/<int:message_id>/delete", delete_message, name="delete-message"),

    path('user/<int:pk>/followers/', FollowListView.as_view(), name='follow-list'),
    path('follow/<int:pk>/', FollowDetailView.as_view(), name='follow-detail'),
    path('follow-toggle/', toggle_follow, name='follow-toggle'),

    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/read/", MarkNotificationAsReadView.as_view(), name="mark-notifications-read"),
]

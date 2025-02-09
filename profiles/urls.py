from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.UsersListView.as_view(), name='users'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user-profile'),
    path('profile/<int:pk>/edit/', UserUpdateView.as_view(), name='user-update'),

    path("chat/<int:receiver_id>/", chat_view, name="chat"),
    path("messages/delete/<int:message_id>/", delete_message, name="delete-message"),

    path('user/<int:pk>/followers/', FollowListView.as_view(), name='follow-list'),
    path('follow/<int:pk>/', FollowDetailView.as_view(), name='follow-detail'),
    path('follow-toggle/', toggle_follow, name='follow-toggle'),

    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/read/", MarkNotificationAsReadView.as_view(), name="mark-notifications-read"),
]

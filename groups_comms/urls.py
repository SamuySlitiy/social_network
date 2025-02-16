from django.urls import path
from .views import *

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),

    path("group/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),

    path("group/<int:group_id>/chat/", GroupMessageListView.as_view(), name="group_chat"),
    path("group/<int:group_id>/send/", SendMessageView.as_view(), name="send_message"),
    path('message/<int:message_id>/edit/', EditMessageView.as_view(), name='edit_message'),
    path('message/<int:message_id>/delete/', DeleteMessageView.as_view(), name='delete_message'),

    path('groups/<int:group_id>/ratings/', RatingListView.as_view(), name='rating_list'),
    path('group/<int:group_id>/rating/<int:pk>/', RatingListView.as_view(), name='rating_detail'),
    path('groups/<int:group_id>/ratings/add/', RatingCreateView.as_view(), name='rating_create'),
    path('group/<int:group_id>/rating/<int:pk>/update/', RatingUpdateView.as_view(), name='rating_update'),
    path('group/<int:group_id>/rating/<int:pk>/delete/', RatingDeleteView.as_view(), name='rating_delete'),
]
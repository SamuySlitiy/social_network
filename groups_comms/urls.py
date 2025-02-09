from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),

    path("group/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("group/<int:group_id>/messages/new/", GroupMessageCreateView.as_view(), name="group_message_create"),
    path("group/messages/<int:pk>/edit/", GroupMessageUpdateView.as_view(), name="group_message_edit"),
    path("group/messages/<int:pk>/delete/", GroupMessageDeleteView.as_view(), name="group_message_delete"),

    path('groups/<int:group_id>/ratings/', RatingListView.as_view(), name='rating_list'),
    path('groups/<int:group_id>/ratings/add/', RatingCreateView.as_view(), name='rating_create'),
    path('groups/<int:group_id>/ratings/<int:pk>/edit/', RatingUpdateView.as_view(), name='rating_update'),
    path('groups/<int:group_id>/ratings/<int:pk>/delete/', RatingDeleteView.as_view(), name='rating_delete'),
]
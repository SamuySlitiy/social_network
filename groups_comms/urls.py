from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', GroupListView.as_view(), name='group_list'),
    path('create/', GroupCreateView.as_view(), name='group_create'),
    path('<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),

    path('<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path('message/<int:pk>/edit/', GroupMessageUpdateView.as_view(), name='group_message_edit'),
    path('message/<int:pk>/delete/', GroupMessageDeleteView.as_view(), name='group_message_delete'),
]
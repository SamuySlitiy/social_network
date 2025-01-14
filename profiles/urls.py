from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UsersListView.as_view(), name='users'),
    #path('', views.messages_view, name='messages'),
    #path('@<str:username>/', views.chat_view, name='chat')
]

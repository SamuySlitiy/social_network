from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('index/', IndexPage.as_view(), name='main-page'),

    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path("posts/<int:post_id>/likes/", LikeListView.as_view(), name="like-list"),
    path("posts/<int:post_id>/like/", LikeCreateView.as_view(), name="like-create"),
    path("posts/<int:post_id>/unlike/", LikeDeleteView.as_view(), name="like-delete"),

    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/<int:post_id>/comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
    path('posts/<int:post_id>/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/create/', NoteCreateView.as_view(), name='note-create'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
]

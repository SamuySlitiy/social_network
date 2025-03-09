from django.contrib import admin
from .models import Note, Post, Comment, Like

admin.site.register((Note, Post, Comment, Like))
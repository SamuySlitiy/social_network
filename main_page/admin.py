from django.contrib import admin
from .models import Note, Post, Comment

admin.site.register((Note, Post, Comment))
from django.contrib import admin
from .models import User, Follow, PrivateMessage, Notification

admin.site.register((User, Follow, PrivateMessage, Notification))

# Register your models here.

from django.contrib import admin
from .models import User, Friendship, Subscription

admin.site.register((User, Friendship, Subscription))

# Register your models here.

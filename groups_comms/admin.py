from django.contrib import admin
from .models import Group, GroupMessage, Rating

admin.site.register((Group, GroupMessage, Rating))



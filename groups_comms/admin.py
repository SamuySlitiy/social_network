from django.contrib import admin
from .models import Group, GroupMessage

admin.site.register((Group, GroupMessage))



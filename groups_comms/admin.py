from django.contrib import admin
from .models import Group, Community

admin.site.register((Group, Community))



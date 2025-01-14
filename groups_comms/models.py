from django.db import models
from profiles.models import User

class Group(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(max_length=255)
    members = models.ManyToManyField(User, related_name='group', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(max_length=255)
    members = models.ManyToManyField(User, related_name='community', blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

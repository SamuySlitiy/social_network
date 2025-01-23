from django.db import models
from profiles.models import User

class Group(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(max_length=255)
    members = models.ManyToManyField(User, related_name='group', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def member_count(self):
        return self.members.count()

    def member_names(self):
        return [member.username for member in self.members.all()]

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name='group_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='media/group_files/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} in {self.group.name}'


'''class Community(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255)
    members = models.ManyToManyField(User, related_name='community', blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name'''
    

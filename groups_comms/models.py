from django.db import models
from profiles.models import User

class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_owner')
    name = models.CharField(max_length=70)
    description = models.TextField(max_length=255)
    members = models.ManyToManyField(User, related_name='group', blank=True)
    is_verified = models.BooleanField(default=False)
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
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='group_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} in {self.group.name}'

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Very Bad'),
        (2, '2 - Bad'),
        (3, '3 - Okay'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    content = models.TextField(max_length=500, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="ratings")

    def __str__(self):
        return f"Rating by {self.user.username} - Score: {self.rating}"
    
    class Meta:
        ordering = ['-created_at']
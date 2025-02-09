from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.CharField(max_length=250, blank=True)
    user_followers = models.ManyToManyField('self', symmetrical=False, related_name='user_follows')

    def __str__(self):
        return self.username
    
    def user_first_name(self):
        return f"First Name: {self.first_name}"
    
    def user_last_name(self):
        return f"Last Name: {self.last_name}"
    
    def user_email(self):
        return f"Email: {self.email}"

class Follow(models.Model):
    is_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    is_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('is_following', 'is_followed')

    def __str__(self):
        return f"{self.is_following.username} follows {self.is_followed.username}"

class PrivateMessage(models.Model):
    senter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_received')
    text = models.TextField(max_length=200)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['senter', 'receiver']),
        ]

    def __str__(self):
        return f"{self.senter.username} has sent {self.receiver.username} a message."
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'Message'),
        ('like', 'Like'),
        ('follow', 'Follow'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"
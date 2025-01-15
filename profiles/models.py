from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.CharField(max_length=250, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def get_friends(self):
        friends = Friendship.objects.filter(models.Q(requester=self, is_accepted=True) | models.Q(receiver=self, is_accepted=True))
        return [f.receiver if f.requester == self else f.requester for f in friends]


    def get_subscriptions(self):
        return Subscription.objects.filter(subscriber=self).values_list('subscribed_to', flat=True)


    def get_subscribers(self):
        return Subscription.objects.filter(subscribed_to=self).values_list('subscriber', flat=True)
    
    def get_messages(self):
        return PrivateMessage.objects.filter(senter=self).values_list('receiver', flat=True)

class Friendship(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('requester', 'receiver') 
        indexes = [
            models.Index(fields=['requester', 'receiver']),
        ]

    def __str__(self):
        return f"{self.requester.username} -> {self.receiver.username} ({'Friends' if self.is_accepted else 'Pending'})"

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')
        indexes = [
            models.Index(fields=['subscriber', 'subscribed_to']),
        ]

    def __str__(self):
        return f"{self.subscriber.username} -> {self.subscribed_to.username}"
    
class PrivateMessage(models.Model):
    senter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_received')
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('senter', 'receiver')
        indexes = [
            models.Index(fields=['senter', 'receiver']),
        ]

    def __str__(self):
        return f"{self.senter.username} has sent {self.receiver.username} a message."
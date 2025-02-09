from .models import Notification

def create_notification(user, sender, notification_type, text):
    Notification.objects.create(
        user=user,
        sender=sender,
        notification_type=notification_type,
        text=text
    )

from django import forms
from .models import User, Friendship, Subscription, PrivateMessage


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'bio']


class FriendshipForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ['receiver']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['subscribed_to']


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['receiver', 'message_content']

    message_content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Message")

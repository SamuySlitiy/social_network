from django import forms
from .models import User, PrivateMessage


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'bio']

class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['text']

    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Message")

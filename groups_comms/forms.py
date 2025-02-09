from django import forms
from .models import Group, GroupMessage, Rating

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'members']

class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['text', 'file']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
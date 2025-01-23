from django import forms
from .models import Group, GroupMessage

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'members']

class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['text', 'file']

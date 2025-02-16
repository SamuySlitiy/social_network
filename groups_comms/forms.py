from django import forms
from .models import Group, GroupMessage, Rating
from profiles.models import User

class GroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    class Meta:
        model = Group
        fields = ['name', 'description', 'members', 'is_verified']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["content", "file"]
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main_page.models import *
from django import forms

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class UserAuthForm(AuthenticationForm):
    class Meta:
        model = User
from django import forms
from django.contrib.auth.models import User
from core.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        field = ('username', 'email', 'password')

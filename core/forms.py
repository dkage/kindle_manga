from django import forms
from django.contrib.auth.models import User
from core.models import UserProfile


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm')

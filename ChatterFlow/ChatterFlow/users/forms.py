from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()  # Add this line if it's missing

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]  # Include 'email' here


class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["username", "email", "image", "bio"]

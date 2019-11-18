from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        fields = ['username', 'email', 'password1', 'password2']
        model = User


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta():
        fields = ['username', 'email']
        model = User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender']

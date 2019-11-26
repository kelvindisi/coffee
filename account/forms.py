from django import forms
from account.models import UserModel as User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    id_number = forms.CharField(max_length=30)

    class Meta():
        fields = ['id_number', 'username', 'email', 'password1', 'password2']
        model = User


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta():
        fields = ['id_number', 'email']
        model = User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender']

from django import forms
from account.models import UserModel
from farmer.models import Product

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'id_number', 'email', 'first_name', 'last_name', 'password']

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity', 'price_per_kg', 'factory']


class SearchUserForm(forms.Form):
    username = forms.CharField(max_length=250)

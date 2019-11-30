from django import forms
from account.models import UserModel
from farmer.models import Product
from .models import Factory, FactoryPrice


class CreateUserForm(forms.ModelForm):
    facts = Factory.objects.all()
    fact_choices = []
    for factory in facts:
        fact_choices.append((factory.id, factory.name))
    factories = forms.CharField(widget=forms.Select(choices=fact_choices))
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['factories', 'id_number', 'email',
                  'first_name', 'last_name', 'password']


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity', 'price_per_kg', 'factory']


class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = ['name', 'email', 'phone_number', 'address']


class CreateFactoryPriceForm(forms.ModelForm):
    price = forms.IntegerField(label="Buying price", widget=forms.NumberInput(
        attrs={
            "min": 0
        }
    ))

    class Meta:
        model = FactoryPrice
        fields = ['price']

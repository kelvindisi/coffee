from django import forms
from account.models import UserModel
from farmer.models import Product, Transaction
from .models import Factory, FactoryPrice


class CreateUserForm(forms.ModelForm):
    fact_choices = []
    try:
        facts = Factory.objects.all()
        for factory in facts:
            fact_choices.append((factory.id, factory.name))
    except:
        fact_choices = []
    factories = forms.CharField(widget=forms.Select(choices=fact_choices))
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['factories', 'id_number', 'email',
                  'first_name', 'last_name', 'password']


class UpdateUserForm(forms.ModelForm):
    fact_choices = []
    try:
        facts = Factory.objects.all()

        for factory in facts:
            fact_choices.append((factory.id, factory.name))
    except:
        fact_choices = []

    factories = forms.CharField(widget=forms.Select(choices=fact_choices))

    class Meta:
        model = UserModel
        fields = ['factories', 'id_number', 'email',
                  'first_name', 'last_name']


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity', 'price_per_kg', 'factory']


class UpdateProductScheduleForm(forms.ModelForm):
    date_scheduled = forms.DateTimeField()

    class Meta:
        model = Product
        fields = ['date_scheduled']


class UpdateProductQuantity(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']


class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = ['name', 'email', 'phone_number', 'address']


class CreateFactoryPriceForm(forms.ModelForm):
    price = forms.IntegerField(label="Buying price (Per Kg)", widget=forms.NumberInput(
        attrs={
            "min": 0
        }
    ))

    class Meta:
        model = FactoryPrice
        fields = ['price']


class PayForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

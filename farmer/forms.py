from django import forms
from .models import Product

class CreateProduceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['factory', 'approximate_quantity']
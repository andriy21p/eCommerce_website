from django.forms import ModelForm, widgets
from ..models import Checkout
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError


class CheckoutForm(ModelForm):
    class Meta:
        model = Checkout
        exclude = []
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'street_address': widgets.TextInput(attrs={'class': 'form-control'}),
            'house_number': widgets.TextInput(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'country': widgets.TextInput(attrs={'class': 'form-control'}),
            'postal_code': widgets.TextInput(attrs={'class': 'form-control'}),

        }
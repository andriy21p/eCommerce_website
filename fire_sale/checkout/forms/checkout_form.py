from django.forms import ModelForm, widgets
from ..models import Checkout



class CheckoutForm(ModelForm):
    class Meta:
        model = Checkout
        exclude = []
        widgets = {
            'name': widgets.HiddenInput(attrs={'class': 'd-none'}),
            'street_address': widgets.TextInput(attrs={'class': 'form-control'}),
            'house_number': widgets.TextInput(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'country': widgets.TextInput(attrs={'class': 'form-control'}),
            'postal_code': widgets.TextInput(attrs={'class': 'form-control'}),
            'item': widgets.HiddenInput(attrs={'class': 'd-none'}),
            'expiration_month': widgets.NumberInput(attrs={'class': 'form-control'}),
            'expiration_year': widgets.NumberInput(attrs={'class': 'form-control'}),
            'credit_card_num': widgets.NumberInput(attrs={'class': 'form-control'}),
            'cvv': widgets.NumberInput(attrs={'class': 'form-control'}),

        }

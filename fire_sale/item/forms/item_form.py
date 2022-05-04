from django.forms import ModelForm, widgets
from item.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['id', 'user', 'hitcount', 'price_fixed', 'show_in_catalog', 'created', 'edited', 'date_ends']
        widgets = {
            'user': widgets.Select(attrs={'class': 'form-control'}),
            'sale_type': widgets.Select(attrs={'class': 'form-control'}),
            'condition': widgets.Select(attrs={'class': 'form-control'}),
            'category': widgets.Select(attrs={'class': 'form-control'}),
            'price_minimum': widgets.NumberInput(attrs={'class': 'form-control'}),
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'date_ends': widgets.SelectDateWidget(attrs={'class': 'form-control'}),
        }

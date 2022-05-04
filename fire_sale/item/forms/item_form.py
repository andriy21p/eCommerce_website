from django.forms import ModelForm, widgets
from item.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['id']

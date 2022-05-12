from django import forms
from django.forms import ModelForm, widgets, CharField
from item.models import Item, Offer, Tag, ItemImage


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['id', 'user', 'hitcount', 'price_fixed', 'show_in_catalog',
                   'created', 'edited', 'date_ends', 'has_accepted_offer']
        fields = ['name', 'sale_type', 'condition', 'category', 'price_minimum', 'description', 'tags']
        widgets = {
            'user': widgets.Select(attrs={'class': 'form-control'}),
            'sale_type': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'condition': widgets.Select(attrs={'class': 'form-control'}),
            'category': widgets.Select(attrs={'class': 'form-control'}),
            'price_minimum': widgets.NumberInput(attrs={'class': 'form-control'}),
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'}),
            'date_ends': widgets.SelectDateWidget(attrs={'class': 'form-control'}),
        }

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags'})
    )


class ItemFormWithUrl(ModelForm):
    image_url = CharField(max_length=10000, required=False, widget=widgets.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Item
        # exclude = ['id', 'user', 'hitcount', 'price_fixed', 'show_in_catalog', 'created', 'edited', 'date_ends']
        fields = ['name', 'image_url', 'sale_type', 'condition', 'category', 'price_minimum', 'description', 'tags']
        widgets = {
            'sale_type': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'condition': widgets.Select(attrs={'class': 'form-control'}),
            'category': widgets.Select(attrs={'class': 'form-control'}),
            'price_minimum': widgets.NumberInput(attrs={'class': 'form-control'}),
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'}),
            'image': widgets.TextInput(attrs={'class': 'form-control'}),
        }

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags'})
    )


class ItemBidForm(ModelForm):

    class Meta:
        model = Offer
        fields = ['item', 'amount', 'accepted']


class ItemUrl(ModelForm):

    class Meta:
        model = ItemImage
        exclude = []

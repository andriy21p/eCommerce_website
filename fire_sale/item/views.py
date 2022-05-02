from django.shortcuts import render
from item.models import Item


# Create your views here.
def index(request):
    return render(request, 'item/index.html', {
        'item': Item.objects.all(),
    })

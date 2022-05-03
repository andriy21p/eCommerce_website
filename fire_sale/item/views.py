from django.shortcuts import render
from item.models import Item


# Create your views here.
def index(request):
    return render(request, 'item/index.html', {
        'items': Item.objects.all(), 'images': Item.itemimage_set,
    })


# @login_required

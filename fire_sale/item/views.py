from django.shortcuts import render
from item.models import Item, ItemCategory


# Create your views here.
def index(request):
    return render(request, 'item/index.html', {
        'items': Item.objects.all(), 'images': Item.itemimage_set, 'categories': ItemCategory.objects.all().order_by('order'),
    })



# @login_required

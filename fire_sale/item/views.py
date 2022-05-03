from django.http import JsonResponse
from django.shortcuts import render
from item.models import Item, ItemCategory


# Create your views here.
def index(request):
    if 'category' in request.GET:
        category = request.GET['category']
        items = [{
            'id': x.id,
            'sale_type_id': x.sale_type_id,
            'sale_type': x.sale_type.name,
            'price_minimum': x.price_minimum,
            'price_fixed': x.price_fixed,
            'condition': x.condition.name,
            'name': x.name,
            'description': x.description,
            'ends': x.date_ends,
            'created': x.created,
            'edited': x.edited,
            'category_id': x.category_id,
            'category': x.category.name,
            'category_icon': x.category.icon,
            'image': x.itemimage_set.first().url,
            'image_description': x.itemimage_set.first().description,
        } for x in Item.objects.filter(show_in_catalog=True,
                                       category__name__icontains=category).order_by('name')]
        return JsonResponse({'items': items})
    return render(request, 'item/index.html', {
        'items': Item.objects.filter(show_in_catalog=True).order_by('name'),
        'images': Item.itemimage_set,
        'categories': ItemCategory.objects.all().order_by('order'),
    })

# @login_required

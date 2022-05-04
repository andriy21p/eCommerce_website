from django.http import JsonResponse
from django.shortcuts import render
from item.models import Item, ItemCategory
from django.db.models import F


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
            'popularity': x.popularity,
        } for x in Item.objects.filter(show_in_catalog=True,
                                       category__name__icontains=category).order_by('name')]
        return JsonResponse({'items': items})
    return render(request, 'item/index.html', {
        'items': Item.objects.filter(show_in_catalog=True).order_by('name'),
        'categories': ItemCategory.objects.all().order_by('order'),
    })


# @login_required
def get_item_by_id(request, item_key):
    Item.objects.filter(id=item_key).update(popularity=F('popularity') + 1)
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
        'popularity': x.popularity,
        'images': [{'url': y.url, 'description': y.description, } for y in x.itemimage_set.all()],
    } for x in Item.objects.filter(pk=item_key)]
    return JsonResponse({'items': items})

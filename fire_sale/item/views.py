from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item, ItemCategory, ItemImage
from item.forms.item_form import ItemForm, ItemFormWithUrl, ItemBidForm
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
            'hitcount': x.hitcount,
            'image': [{'url': y.url, 'description': y.description, } for y in x.itemimage_set.all()],
            'current_price': x.current_price(),
            'number_of_bids': x.number_of_offers(),
        } for x in Item.objects.filter(show_in_catalog=True,
                                       category__name__icontains=category).order_by('-hitcount', 'name')]
        return JsonResponse({'items': items})

    if 'search' in request.GET:
        search = request.GET['search']
        return render(request, 'item/index.html', {
            'items': Item.objects.filter(show_in_catalog=True, name__icontains=search).order_by('-hitcount', 'name'),
            'categories': ItemCategory.objects.all().order_by('order'),
        })

    return render(request, 'item/index.html', {
        'items': Item.objects.filter(show_in_catalog=True).order_by('-hitcount','name'),
        'categories': ItemCategory.objects.all().order_by('order'),
    })


def get_item_by_id(request, item_key):
    Item.objects.filter(id=item_key).update(hitcount=F('hitcount') + 1)
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
        'hitcount': x.hitcount,
        'images': [{'url': y.url, 'description': y.description, } for y in x.itemimage_set.all()],
        'current_price': x.current_price(),
        'number_of_bids': x.number_of_offers(),
    } for x in Item.objects.filter(pk=item_key)]
    return JsonResponse({'items': items})


@login_required
def create(request):
    if request.method == "POST":
        form = ItemFormWithUrl(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            if 'image_url' in request.POST:
                new_image = ItemImage()
                new_image.url = request.POST['image_url']
                new_image.item = new_item
                new_image.save()
            return redirect("my-profile")
    return render(request, "item/item_create.html", {
        "form": ItemFormWithUrl()
    })


@login_required
def edit(request, item_key):
    item = get_object_or_404(Item, pk=item_key)
    if request.POST:
        form = ItemForm(instance=item, data=request.POST)
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.edited = timezone.now()
            newItem.save()
            return redirect('my-profile')
    return render(request, 'item/item_edit.html', {
        'form': ItemForm(instance=item)
    })


@login_required
def bid(request, item_key):

    item = get_object_or_404(Item, pk=item_key)
    if request.POST and ('amount' in request.POST):
        form = ItemBidForm(data=request.POST)
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.offer_by = request.user
            newItem.save()
            return redirect('my-profile')
    return render(request, 'item/', {
    })

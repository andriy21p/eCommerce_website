from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item, ItemCategory, ItemImage, Offer
from item.forms.item_form import ItemForm, ItemFormWithUrl, ItemBidForm
from message.forms.msg_form import MsgReplyForm
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test


# check if user is owner of item
def user_owns_item(user):
    return True


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
    # print(Item.objects.filter(show_in_catalog=True).order_by('-hitcount', 'name').query);
    return render(request, 'item/index.html', {
        'items': Item.objects.filter(show_in_catalog=True).order_by('-hitcount', 'name'),
        'categories': ItemCategory.objects.all().order_by('order'),
    })


def get_item_by_id(request, item_key):
    Item.objects.filter(id=item_key).exclude(user=request.user).update(hitcount=F('hitcount') + 1)
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
    if item.user != request.user:
        return redirect("my-profile")
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
    if request.POST and ('amount' in request.POST):
        form = ItemBidForm(data=request.POST)
        if form.is_valid():
            new_item_bid = form.save(commit=False)
            new_item_bid.offer_by = request.user
            new_item_bid.save()
            new_item = Item.objects.filter(pk=item_key).first()
            new_sender = request.user
            new_offer = Offer.objects.filter(offer_by=new_sender).latest('created')
            new_receiver = Item.objects.filter(pk=item_key).first().user

            form_msg = MsgReplyForm(data={'sender': new_sender,
                                          'receiver': new_receiver,
                                          'item': new_item,
                                          'offer': new_offer,
                                          'msg_subject': str(new_offer),
                                          'msg_body': 'Do something!'})
            if form_msg.is_valid():
                form_msg.save()
            return redirect('my-profile')
    return render(request, 'item/', {
    })


def accept_item_bid(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.user == offer.item.user:
        # 1. accept offer and congratulate the winner
        offer.accepted = True
        form_msg = MsgReplyForm(data={'sender': request.user,
                                      'receiver': offer.offer_by,
                                      'item': offer.item,
                                      'offer': offer,
                                      'msg_subject': 'You just had the highest bid for ' + offer.item.name + ' !',
                                      'msg_body': 'Congratulations ! Now it''s time to pay up!'})
        if form_msg.is_valid():
            form_msg.save()

        # 2. reject all other offers
        rejected_offers = Offer.objects.filter(item=offer.item).exclude(pk=offer_id).order_by('-created')
        for offer in rejected_offers:
            # mark offer as rejected
            offer.valid = False
            # send notification to bidder that offer was rejected
            form_msg = MsgReplyForm(data={'sender': request.user,
                                          'receiver': offer.offer_by,
                                          'item': offer.item,
                                          'offer': offer,
                                          'msg_subject': 'So sorry, your offer for ' + offer.item.name + ' was rejected',
                                          'msg_body': 'Try searching again for ' + offer.item.name})
            if form_msg.is_valid():
                form_msg.save()
            offer.save()
    return None

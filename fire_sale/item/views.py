from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item, ItemCategory, ItemImage, Offer
from item.forms.item_form import ItemForm, ItemFormWithUrl, ItemBidForm
from message.forms.msg_form import MsgReplyForm
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator


# check if user is owner of item
def user_owns_item(user, item):
    if item.user == user:
        return True
    return False


def current_user_if_authenticated(request):
    if request.user.is_authenticated:
        return request.user.id
    return -1


# Create your views here.
def index(request):
    page_number = request.GET.get('page')
    items_per_page = 100
    if 'items' in request.GET:
        try:
            items_per_page = int(request.GET.get('items'))
        except ValueError:
            items_per_page = 15  # the default

    sort_order = 0
    if 'sortorder' in request.COOKIES:
        sort_order = request.COOKIES.get('sortorder')

    first_order = "-hitcount"
    if sort_order == "1":
        first_order = 'hitcount'
    elif sort_order == "2":
        first_order = 'price_minimum'
    elif sort_order == "3":
        first_order = '-price_minimum'
    elif sort_order == "4":
        first_order = 'name'
    elif sort_order == "5":
        first_order = '-name'

    if 'category' in request.GET:
        category = request.GET['category']
        items = [{
            'id': x.id,
            # 'sale_type_id': x.sale_type_id,
            # 'sale_type': x.sale_type.name,
            'price_minimum': x.price_minimum,
            # 'price_fixed': x.price_fixed,
            'condition': x.condition.name,
            'name': x.name,
            'description': x.description,
            'ends': x.date_ends,
            # 'created': x.created,
            # 'edited': x.edited,
            'category_id': x.category_id,
            'category': x.category.name,
            'category_icon': x.category.icon,
            'hitcount': x.hitcount,
            'images': [{'url': y.url, 'description': y.description, } for y in x.itemimage_set.all()],
            'current_price': x.current_price(),
            'number_of_bids': x.number_of_offers(),
            'seller': x.user.id,
            'current_user': current_user_if_authenticated(request),
            'current_highest_bidder': x.current_winning_user_id(),
            'sort': x.sort_order(),
            'tags': [{'id': y.id, 'name': y.name, } for y in x.tags.all()],
        } for x in Item.objects.filter(show_in_catalog=True, has_accepted_offer=False,
                                       category__name__icontains=category).order_by(first_order, '-hitcount', 'name')
            .select_related('user', 'user__profile', 'sale_type', 'condition', 'category')
            .prefetch_related('itemimage_set', 'offer_set', 'offer_set__offer_by', 'user__offer_set', 'tags')]
        return JsonResponse({'items': items})

    if 'search' in request.GET:
        search = request.GET['search']
        items = Item.objects.filter(show_in_catalog=True,
                                    has_accepted_offer=False,
                                    name__icontains=search).order_by(first_order, '-hitcount', 'name') \
            .select_related('user', 'user__profile', 'sale_type', 'condition', 'category') \
            .prefetch_related('itemimage_set', 'offer_set', 'offer_set__offer_by', 'user__offer_set', 'tags')
        paginator = Paginator(items, items_per_page)
        page_obj = paginator.get_page(page_number)
        return render(request, 'item/index.html', {
            'items': page_obj,
            'search': '&search=' + search,
            'categories': ItemCategory.objects.all().order_by('order'),
        })

    # going to the default items handler
    items = Item.objects.filter(show_in_catalog=True,
                                has_accepted_offer=False).order_by(first_order, '-hitcount', 'name') \
        .select_related('user', 'user__profile', 'sale_type', 'condition', 'category') \
        .prefetch_related('itemimage_set', 'offer_set', 'offer_set__offer_by', 'user__offer_set', 'tags')
    paginator = Paginator(items, items_per_page)
    page_obj = paginator.get_page(page_number)
    return render(request, 'item/index.html', {
        'items': page_obj,
        'search': '',
        'categories': ItemCategory.objects.all().order_by('order'),
    })


def get_item_by_id(request, item_key):
    Item.objects.filter(id=item_key) \
        .exclude(user=current_user_if_authenticated(request)) \
        .update(hitcount=F('hitcount') + 1)
    items = [{
        'id': x.id,
        # 'sale_type_id': x.sale_type_id,
        # 'sale_type': x.sale_type.name,
        'price_minimum': x.price_minimum,
        # 'price_fixed': x.price_fixed,
        'condition': x.condition.name,
        'name': x.name,
        'description': x.description,
        'ends': x.date_ends,
        # 'created': x.created,
        # 'edited': x.edited,
        'category_id': x.category_id,
        'category': x.category.name,
        'category_icon': x.category.icon,
        'hitcount': x.hitcount,
        'images': [{'url': y.url, 'description': y.description, } for y in x.itemimage_set.all()],
        'current_price': x.current_price(),
        'number_of_bids': x.number_of_offers(),
        'seller': x.user.id,
        'current_user': current_user_if_authenticated(request),
        'current_highest_bidder': x.current_winning_user_id(),
        'sort': x.sort_order(),
        'tags': [{'id': y.id, 'name': y.name, } for y in x.tags.all()],
    } for x in Item.objects.filter(pk=item_key)]
    return JsonResponse({'items': items})


@login_required
def create(request):
    if request.method == "POST":
        formdata = request.POST.copy()
        formdata['sale_type'] = 1
        form = ItemFormWithUrl(data=formdata)
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
        'form': ItemFormWithUrl()
    })


@login_required
def edit(request, item_key):
    item = get_object_or_404(Item, pk=item_key)
    if not request.user.is_authenticated:
        return redirect('item-index')
    if item.user != request.user:
        return redirect('my-profile')
    if request.POST:
        form = ItemForm(instance=item, data=request.POST)
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.edited = timezone.now()
            newItem.save()
            return redirect('my-profile')
    return render(request, 'item/item_edit.html', {
        'form': ItemForm(instance=item),
        'item': item,
    })


@login_required
def delete(request, item_key):
    item = get_object_or_404(Item, pk=item_key)
    if not request.user.is_authenticated:
        return redirect('item-index')
    if item.user != request.user:
        return redirect('my-profile')
    form = get_object_or_404(Item, pk=item_key)
    form.delete()
    return redirect('my-profile')


@login_required
def bid(request, item_key):
    if not request.user.is_authenticated:
        return redirect('item-index')
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


@login_required
def offers(request, item_key):
    item = get_object_or_404(Item, pk=item_key)
    return render(request, 'item/item_offers.html', {
        'item': item,
        'offers': item.offer_set.filter(valid=True).order_by('-amount')
    })


def accept_item_bid(request, offer_id):
    if not request.user.is_authenticated:
        return redirect('item-index')
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
                                          'msg_subject': 'So sorry, your offer for ' +
                                                         offer.item.name + ' was rejected',
                                          'msg_body': 'Try searching again for ' + offer.item.name})
            if form_msg.is_valid():
                form_msg.save()
            offer.save()

        # 3. merkjum item sem selt svo það birtist ekki lengur í catalog
        item = offer.item
        item.has_accepted_offer = True
        item.save()
    return None


def similar(request, item_key):
    """
        Returns JSON of similar items
    """
    number_of_similar_items_max = 4
    selected = Item.objects.filter(pk=item_key).first()
    items = [{
        'id': x.id,
        # 'sale_type_id': x.sale_type_id,
        # 'sale_type': x.sale_type.name,
        'price_minimum': x.price_minimum,
        # 'price_fixed': x.price_fixed,
        'condition': x.condition.name,
        'name': x.name,
        'description': x.description,
        # 'ends': x.date_ends,
        # 'created': x.created,
        'edited': x.edited,
        'category_id': x.category_id,
        'category': x.category.name,
        'category_icon': x.category.icon,
        'hitcount': x.hitcount,
        'images': [{'url': y.url, 'description': y.description, } for y in x.itemimage_set.all()],
        'current_price': x.current_price(),
        'number_of_bids': x.number_of_offers(),
        'seller': x.user.id,
        'current_user': current_user_if_authenticated(request),
        'current_highest_bidder': x.current_winning_user_id(),
        'sort': x.sort_order(),
        'tags': [{'id': y.id, 'name': y.name, } for y in x.tags.all()],
    } for x in Item.objects.filter(category=selected.category,
                                   show_in_catalog=True,
                                   has_accepted_offer=False)
                   .exclude(pk=item_key)
                   .order_by('-hitcount')[0:number_of_similar_items_max]
        .select_related('user', 'user__profile', 'sale_type', 'condition', 'category')
        .prefetch_related('itemimage_set', 'offer_set', 'offer_set__offer_by', 'user__offer_set', 'tags')
    ]
    return JsonResponse({'items': items})

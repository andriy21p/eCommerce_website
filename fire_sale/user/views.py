from django.shortcuts import render, redirect, get_object_or_404
from user.forms.profile_form import ProfileForm
from user.models import User, Profile, Footer
from item.models import Item, Offer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    page_number = request.GET.get('page')
    items_per_page = 12
    if 'items' in request.GET:
        try:
            items_per_page = int(request.GET.get('items'))
        except ValueError as verr:
            items_per_page = 16  # the default
    offersForMyItems = [{
        'numberOfBids': x.item.number_of_offers(),
        'highest': x.item.current_price(),
        'highestUser': x.item.current_winning_user,
        'item': x.item,
        'bids': [{
            'user': y.offer_by,
            'amount': y.amount,
            'offer_time': y.created,
        } for y in Offer.objects.filter(item=x.item, valid=True)
                                        .order_by('-amount', 'created')
                                        .prefetch_related('offer_by')[0:10]],
    } for x in Offer.objects.filter(item__user=request.user, valid=True, item__has_accepted_offer=False)
        .distinct('item')
        .prefetch_related('offer_by', 'item')
        .select_related('item')]

    myOffers = [{
        'myOfferDetails': x.get_highest_by_user(request.user),
        'numberOfBids': x.item.number_of_offers(),
        'highest': x.item.current_price(),
        'highestUser': x.item.current_winning_user,
        'item': x.item,
    } for x in Offer.objects.filter(offer_by=request.user, item__has_accepted_offer=False)
        .distinct('item')
        .prefetch_related('offer_by', 'item')]

    myItemsToShip = [{
        'myOfferDetails': x.get_highest_by_user(request.user),
        'numberOfBids': x.item.number_of_offers(),
        'highest': x.item.current_price(),
        'highestUser': x.item.current_winning_user,
        'item': x.item,
    } for x in Offer.objects.filter(item__user=request.user, item__has_accepted_offer=True, checkout__is_confirmed=True)
        .distinct('item')
        .prefetch_related('offer_by', 'item', 'checkout')]

    # going to the default items handler
    items = Item.objects.filter(user=request.user, has_accepted_offer=False)\
        .order_by('-hitcount', 'created')\
        .select_related('user', 'user__profile', 'sale_type', 'condition', 'category')\
        .prefetch_related('itemimage_set', 'offer_set', 'offer_set__offer_by', 'user__offer_set', 'tags')
    paginator = Paginator(items, items_per_page)
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/index.html', {
        'users': User.objects.filter(pk=request.user.id),
        'myItems': page_obj,
        'myOffers': myOffers,
        'myItemsToShip': myItemsToShip,
        'offersForMyItems': offersForMyItems,
    })


def other_profile(request, user_id):
    if request.user.id == user_id:
        return redirect('my-profile')
    page_number = request.GET.get('page')
    items_per_page = 12
    if 'items' in request.GET:
        try:
            items_per_page = int(request.GET.get('items'))
        except ValueError as verr:
            items_per_page = 12  # the default

    items = Item.objects.filter(user=user_id, has_accepted_offer=False).order_by('-hitcount', 'created')\
        .select_related('user', 'user__profile', 'sale_type', 'condition', 'category')\
        .prefetch_related('itemimage_set', 'offer_set', 'offer_set__offer_by', 'user__offer_set', 'tags')
    paginator = Paginator(items, items_per_page)
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/other_profile.html', {
        'users': User.objects.filter(pk=user_id),
        'offeredItems': page_obj,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'user/register.html', {
        'form': UserCreationForm()
    })


def profile(request):
    input_profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProfileForm(instance=input_profile, data=request.POST)
        if form.is_valid():
            temp_profile = form.save(commit=False)
            temp_profile.user = request.user
            temp_profile.save()
            return redirect('profile')
    return render(request, 'user/profile.html', {
        'form': ProfileForm(instance=input_profile)
    })


@login_required
def image(request):
    input_profile = Profile.objects.filter(user=request.user).first()
    if request.POST:
        user = get_object_or_404(User, pk=request.user.id)
        user.email = request.POST['email']
        user.first_name = request.POST['name']
        user.profile.bio = request.POST['bio']
        user.save()
        form = ProfileForm(instance=input_profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
    return render(request, 'user/image.html', {
        'form': input_profile
    })


def conduct(request):
    footer_links = Footer.objects.filter(footer_page=1).order_by("-created").first()
    return render(request, 'user/codeofconduct.html', {
        'footer': footer_links,
        })


def cookies(request):
    footer_links = Footer.objects.filter(footer_page=4).order_by("-created").first()
    return render(request, 'user/cookies.html', {
        'footer': footer_links,
        })


def security(request):
    footer_links = Footer.objects.filter(footer_page=3).order_by("-created").first()
    return render(request, 'user/security.html', {
        'footer': footer_links,
        })


def privacy(request):
    footer_links = Footer.objects.filter(footer_page=2).order_by("-created").first()
    return render(request, 'user/privacy.html', {
        'footer': footer_links,
        })


def help(request):
    footer_links = Footer.objects.filter(footer_page=5).order_by("-created").first()
    return render(request, 'user/help.html', {
        'footer': footer_links,
        })


def advice(request):
    footer_links = Footer.objects.filter(footer_page=6).order_by("-created").first()
    return render(request, 'user/advice.html', {
        'footer': footer_links,
        })

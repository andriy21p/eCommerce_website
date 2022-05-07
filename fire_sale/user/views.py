from django.shortcuts import render, redirect

from user.forms.profile_form import ProfileForm
from user.models import User, Profile
from item.models import Item, Offer
from message.models import Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def index(request):
    items = [{
        'myOfferDetails': x.get_highest_by_user(request.user),
        'numberOfBids': x.item.number_of_offers(),
        'highest': x.item.current_price(),
        'highestUser': x.item.current_winning_user(),
        'item': x.item,
    } for x in Offer.objects.filter(offer_by=request.user).distinct('item')]
    return render(request, 'user/index.html', {
        'users': User.objects.filter(pk=request.user.id),
        'myItems': Item.objects.filter(user=request.user).order_by('-hitcount', 'created'),
        'myOffers': items,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logingiot')
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
        form = ProfileForm(instance=input_profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
    return render(request, 'user/image.html', {
        'form': input_profile
    })

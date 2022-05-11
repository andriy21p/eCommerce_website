from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms.checkout_form import CheckoutForm, UserReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from checkout.models import Checkout
from item.models import Offer


# Create your views here.
@login_required
def index(request, order_id):

    current_user = request.user
    order = get_object_or_404(Offer, pk=order_id)
    return render(request, "checkout/index.html", {
        "Checkout": Checkout.objects.filter(name=current_user.id),
        'order': order
    })


def get_checkout_by_id(request, checkout_id):
    #checkout = get_object_or_404(Checkout, pk=checkout_id)
    checkout = [{
        #"id": co_entry.id,
        #"offer_id": co_entry.offer_id,
        "Street Address:": co_entry.street_address,
        "House Number:": co_entry.house_number,
        "City:": co_entry.city,
        "Country:": co_entry.country,
        "Postal Code:": co_entry.postal_code,
        "Credit card holder:": co_entry.credit_card_holder,
        "Credit card number:": co_entry.credit_card_number,
        "Expiration month:": co_entry.expiration_month,
        "Expiration year:": co_entry.expiration_year,
        "CVV:": co_entry.cvv,
        #"is_confirmed": co_entry.is_confirmed
    } for co_entry in Checkout.objects.filter(pk=checkout_id)]
    return render(request, 'checkout/preview.html', {"checkout": checkout})


def register_checkout(request, order_id):
    order = get_object_or_404(Offer, pk=order_id)
    if order.offer_by != request.user:
        return redirect('my-profile')

    if request.method == 'POST':
        formdata = request.POST.copy()
        formdata['offer'] = order.offer_by.pk
        form = CheckoutForm(data=formdata)
        if form.is_valid():
            new_checkout = form.save()
            return redirect('preview', checkout_id=new_checkout.pk)

    orderinstance = {'name': order.offer_by.pk, 'item': order.item_id}
    return render(request, 'checkout/index.html', {
        'item': order_id,
        'form': CheckoutForm(initial=orderinstance),
        'order': order,
    })


def user_review(request, checkout_id):
    if request.method == "POST":
        form = UserReviewForm(data=request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.save()
    return render(request, "checkout/user_review.html", {
        "form": form
    })


from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms.checkout_form import CheckoutForm, UserReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from checkout.models import Checkout, get_year_choice
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


def mask_card(card):
    return str(card)[0:2] + '** **** **** ' + str(card)[-4:]


def get_checkout_by_id(request, checkout_id):
    months = dict(Checkout.MONTH_CHOICE)
    years = dict(get_year_choice())
    checkout = [{
        "id": co_entry.id,
        "offer_id": co_entry.offer_id,
        "Street Address:": co_entry.street_address,
        "House Number:": co_entry.house_number,
        "City:": co_entry.city,
        "Country:": co_entry.country,
        "Postal Code:": co_entry.postal_code,
        "Credit card holder:": co_entry.credit_card_holder,
        "Credit card number:": mask_card(co_entry.credit_card_number),
        "Expiration month:": months[co_entry.expiration_month],
        "Expiration year:": years[co_entry.expiration_year],
        "CVV:": co_entry.cvv,
        # "is_confirmed": co_entry.is_confirmed
    } for co_entry in Checkout.objects.filter(pk=checkout_id)]
    return render(request, 'checkout/preview.html', {"checkout": checkout})


def register_checkout(request, order_id):
    order = get_object_or_404(Offer, pk=order_id)
    checkout = Checkout.objects.filter(offer_id=order_id).first()
    if order.offer_by != request.user:
        return redirect('my-profile')

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['offer'] = order.id
        form = CheckoutForm(instance=checkout, data=form_data)
        if form.is_valid():
            form.save()
            checkout = Checkout.objects.filter(offer_id=order_id).first()
            offer = Offer.objects.get(id=order_id)
            offer.checkout_id = checkout.id
            offer.save()
            return redirect('preview', checkout_id=checkout.id)
    checkoutForm = CheckoutForm(instance=checkout)
    return render(request, 'checkout/index.html', {
        'form': checkoutForm,
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

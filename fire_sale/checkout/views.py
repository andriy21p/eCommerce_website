from django.contrib.auth.decorators import login_required
from checkout.forms.checkout_form import CheckoutForm, UserReviewForm
from message.forms.msg_form import MsgReplyForm
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


@login_required
def get_checkout_by_id(request, checkout_id):
    months = dict(Checkout.MONTH_CHOICE)
    years = dict(get_year_choice())
    checkout = [{
        "id": co_entry.id,
        "checkout_id": checkout_id,
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


@login_required
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
            return redirect('preview', checkout_id=checkout.id)
    checkoutForm = CheckoutForm(instance=checkout)
    return render(request, 'checkout/index.html', {
        'form': checkoutForm,
        'order': order,
    })


@login_required
def checkout_complete(request, checkout_id):
    checkout = get_object_or_404(Checkout, pk=checkout_id)
    if checkout.offer.offer_by != request.user:
        return redirect('my-profile')

    if checkout.is_confirmed:
        return redirect('review', checkout_id=checkout_id)

    # save that checkout is completed
    checkout.is_confirmed = True
    checkout.save()

    # send message to seller and buyer about successful checkout
    form_msg = MsgReplyForm(data={'sender': request.user,
                                  'receiver': checkout.offer.item.user,
                                  'item': checkout.offer.item,
                                  'offer': checkout.offer,
                                  'msg_subject': 'Payment completed',
                                  'msg_body': 'Ship \'' + checkout.offer.item.name + '\' to: ' +
                                  checkout.offer.offer_by.first_name + ' ' + checkout.offer.offer_by.last_name + ', ' +
                                  checkout.street_address + ' ' + checkout.house_number + ', ' +
                                  checkout.postal_code + ' ' + checkout.city + ', ' +
                                  checkout.country.countryName+' '
                                  })
    if form_msg.is_valid():
        form_msg.save()

    form_msg = MsgReplyForm(data={'sender': checkout.offer.item.user,
                                  'receiver': request.user,
                                  'item': checkout.offer.item,
                                  'offer': checkout.offer,
                                  'msg_subject': 'Shipment processing has started',
                                  'msg_body': 'We are preparing to ship \'' + checkout.offer.item.name + '\' to: ' +
                                  checkout.offer.offer_by.first_name + ' ' + checkout.offer.offer_by.last_name + ', ' +
                                  checkout.street_address + ' ' + checkout.house_number + ', ' +
                                  checkout.postal_code + ' ' + checkout.city + ', ' +
                                  checkout.country.countryName+' '
                                  })
    if form_msg.is_valid():
        form_msg.save()

    # redirect to review site
    return redirect('review', checkout_id=checkout_id)


@login_required
def user_review(request, checkout_id):
    checkout = get_object_or_404(Checkout, pk=checkout_id)
    if request.method == "POST":
        form = UserReviewForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    seller = checkout.offer.item.user
    buyer = checkout.offer.offer_by.get_full_name()
    item = checkout.offer.item
    form = UserReviewForm(initial={'checkout': checkout, 'seller': seller})
    return render(request, "checkout/user_review.html", {
        "form": form,
        "seller": seller.get_full_name(),
        "buyer": buyer,
        "item": item,
        "checkout_id": checkout_id
    })


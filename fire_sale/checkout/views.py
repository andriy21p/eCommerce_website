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


def register_checkout(request, order_id):
    order = get_object_or_404(Offer, pk=order_id)
    if order.offer_by != request.user:
        return redirect('item/' + order_id)
    if request.method == 'POST':
        formdata = request.POST.copy()
        formdata['name'] = order.offer_by.pk
        formdata['item'] = order.item_id
        form = CheckoutForm(data=formdata)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
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


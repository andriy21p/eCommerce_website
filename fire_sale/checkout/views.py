from django.contrib.auth.decorators import login_required
from .forms.checkout_form import CheckoutForm
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


def register_checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('item')
    return render(request, 'checkout/index.html', {
        'form': CheckoutForm()
    })

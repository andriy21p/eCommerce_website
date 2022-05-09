from django.contrib.auth.decorators import login_required
from .forms.checkout_form import CheckoutForm
from django.shortcuts import render, redirect, get_object_or_404
from ..checkout.models import Checkout

# Create your views here.
@login_required
def index(request):
    """ When a message is requested, when a user is logged, all messages related to him will be displayed."""
    current_user = request.user
    return render(request, "checkout/index.html", {
        "Checkout": Checkout.objects.filter(receiver=current_user.id)
    })


def register_checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logingiot')
    return render(request, 'checkout/index.html', {
        'form': CheckoutForm()
    })
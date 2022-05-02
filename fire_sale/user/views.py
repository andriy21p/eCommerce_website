from django.shortcuts import render, redirect
from user.models import User, Profile
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'user/index.html', {
        'users': User.objects.all(),
    })



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST, instance=request.user)
        profile_form = Profile(request.user.profile)
        if form.is_valid():
            form.save()
        elif profile_form.is_valid():
            profile_form.save()
        return redirect('login')
    return render(request, 'user/register.html', {
        'form': UserCreationForm()
    })

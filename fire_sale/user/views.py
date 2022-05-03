from django.shortcuts import render, redirect

from user.forms.profile_form import ProfileForm
from user.models import User, Profile
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'user/index.html', {
        'users': User.objects.all(),
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

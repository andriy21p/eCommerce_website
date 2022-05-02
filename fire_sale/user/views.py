from django.shortcuts import render
from user.models import User


# Create your views here.
def index(request):
    return render(request, 'user/index.html', {
         'users': User.objects.all(),
    })

# Create your views here.

from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'user/index.html', {
        # 'items': Items.objects.all(),
    })

# Create your views here.

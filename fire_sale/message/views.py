from django.shortcuts import render
# from message.models import Message


# Create your views here.
def index(request):
    return render(request, 'message/index.html', {
        # 'message': Message.objects.all(),
    })



# @login_required

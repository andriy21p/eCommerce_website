from django.shortcuts import render
# from message.models import Message

from django.http import HttpResponseRedirect

from message.forms.forms import MsgReplyForm


# Create your views here.
def index(request):
    return render(request, 'message/index.html', {
        # 'message': Message.objects.all(),
    })


def create_new_msg(request):
    pass


# @login_required

from django.http import JsonResponse
from django.shortcuts import render, redirect
from message.models import Message
from message.forms.msg_form import MsgReplyForm

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
@login_required
def index(request):
    return render(request, 'message/index.html', {
        # 'message': Message.objects.all(),
    })


def create_new_msg(request):
    if request.method == 'POST':
        form = MsgReplyForm(data=request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.save()
            return redirect('my-profile')
    return render(request, 'message/msg_create.html', {
        'form': MsgReplyForm()
    })


def get_msg_by_id(request, msg_key):
    Message.objects.filter(id=msg_key)
    messages = [{
        'id': msg.id,
        'msg_body': msg.message_body,
        'msg_sender': msg.sender.username,
        'msg_receiver': msg.receiver.username,
        'msg_subject': msg.msg_subject,
        'msg_sent': msg.msg_sent,
        'msg_received': msg.msg_received,
        'msg_replied': msg.msg_replied

    } for msg in Message.objects.filter(pk=msg_key)]
    return JsonResponse({'messages': messages})

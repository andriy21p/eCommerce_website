from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from message.models import Message
from message.forms.msg_form import MsgReplyForm, MsgItemOfferAccept, MsgReplyModal
from item.views import accept_item_bid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
@login_required
def index(request):
    """ When a message is requested, when a user is logged, all messages related to him will be displayed."""
    current_user = request.user
    return render(request, "message/index.html", {
        "messages": Message.objects.filter(receiver=current_user.id).order_by("-msg_sent"),
    })


def create_new_msg(request):
    if request.method == "POST":
        form = MsgReplyForm(data=request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.save()
            return redirect("my-profile")
    return render(request, "message/msg_create.html", {
        "form": MsgReplyForm()
    })


def get_msg_by_id(request, msg_key):
    Message.objects.filter(id=msg_key)
    messages = [{
        "id": msg.id,
        "msg_body": msg.msg_body,
        "msg_sender": msg.sender.username,
        "msg_receiver": msg.receiver.username,
        "msg_subject": msg.msg_subject,
        "msg_sent": msg.msg_sent,
        "msg_received": msg.msg_received,
        "msg_replied": msg.msg_replied,
        "item_id": msg.item_id,
        "offer_id": msg.offer_id

    } for msg in Message.objects.filter(pk=msg_key)]
    return JsonResponse({"messages": messages})


def accept_bid(request, msg_key):
    msg = get_object_or_404(Message, pk=msg_key)
    if request.POST:
        form = MsgItemOfferAccept(instance=msg, data=request.POST)
        if form.is_valid():
            msg_accepted = form.save(commit=False)
            msg_accepted.offer.accepted = True
            msg_accepted.offer.save()
            accept_item_bid(request, msg.offer_id)   # Sendir öll notifications
            return redirect('message')

    return render(request, 'message', {
        'form': MsgItemOfferAccept(instance=msg)
    })


def reject_bid(request, msg_key):
    msg = get_object_or_404(Message, pk=msg_key)
    if request.POST:
        form = MsgItemOfferAccept(instance=msg, data=request.POST)
        if form.is_valid():
            msg_accepted = form.save(commit=False)
            msg_accepted.offer.valid = False
            msg_accepted.offer.save()
            return redirect('message')


def msg_reply(request, msg_key):
    if request.method == "POST":
        form = MsgReplyModal(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204)
    else:
        form = MsgReplyModal()
    return render(request, 'message/msg_reply.html', {
        'form': form,
    })

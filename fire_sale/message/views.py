from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from message.models import Message
from message.forms.msg_form import MsgReplyForm, MsgItemOfferAccept, MsgReplyModal, MsgCreate
from item.views import accept_item_bid
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import timedelta
from user.models import User


# Create your views here.
@login_required
def index(request):
    """ When a message is requested, when a user is logged, all messages related to him will be displayed."""
    current_user = request.user
    messages = Message.objects.filter(receiver=current_user.id).order_by("-msg_sent")\
        .select_related('sender', 'receiver', 'item', 'offer')\
        .prefetch_related('msg_next')
    msg_count = messages.count()
    # Paginator initiated. Set to 15 msg per page.
    page_number = request.GET.get('page')
    msg_per_page = 15
    paginator = Paginator(messages, msg_per_page)
    page_obj = paginator.get_page(page_number)
    # mark all unread messages as read
    [{'mark_read': x.mark_read()} for x in Message.objects.filter(receiver=current_user.id, msg_received__isnull=True)]
    return render(request, "message/index.html", {
        "messages": page_obj,
        "msg_count": msg_count
    })


@login_required
def create_new_msg(request, to_user_id):
    to_user = User.objects.filter(pk=to_user_id).first()
    msg = {'sender': request.user, 'receiver': to_user, }
    if request.method == "POST":
        form = MsgCreate(data=request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = to_user
            new_message.save()
            return redirect("message")

    message = MsgCreate(msg)
    return render(request, "message/msg_create.html", {
        "form": message
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
    msg = get_object_or_404(Message, pk=msg_key)
    if request.method == "POST":
        form = MsgReplyModal(data=request.POST)
        new_message = MsgReplyForm()
        if form.is_valid():
            reply = new_message.save(commit=False)
            reply.msg_body = form.cleaned_data["msg_body"]
            reply.msg_subject = msg.msg_subject
            reply.msg_replied = timezone.now()
            reply.receiver = msg.sender
            reply.sender = msg.receiver
            reply.save()
            return HttpResponse("message",
                                status=204)
    else:
        form = MsgReplyModal()
    return render(request, "message/msg_reply.html", {
        "form": form,
    })


def number_of_unread(request):
    """
          Returns a JSON for the front-end with the current message count and
          information about the newest message (for toast)

          This must be super-fast :)  It's called about once every 30 seconds from every client
    """
    errorResponse = JsonResponse({"number_of_unread_messages": 0,
                                  "latest_from": '',
                                  "latest_subject": '',
                                  "latest_date": '',
                                  "show_toast": False})

    if not request.user.is_authenticated:
        return errorResponse

    messages = Message.objects.filter(receiver=request.user, msg_received__isnull=True).count()
    latest_message = Message.objects.filter(receiver=request.user, msg_received__isnull=True)\
        .order_by('-msg_sent').first()

    if latest_message is not None:
        show_toast = (latest_message.msg_sent + timedelta(seconds=30)) > timezone.now()
        return JsonResponse({"number_of_unread_messages": messages,
                             "latest_from": latest_message.sender.username,
                             "latest_subject": latest_message.msg_subject,
                             "latest_date": latest_message.msg_sent,
                             "show_toast": show_toast})

    return errorResponse

from django.db import models
from django.contrib.auth.models import User
from item.models import Item, Offer


# Create your models here.


class Message(models.Model):
    msg_body = models.CharField(max_length=10000)
    sender = models.ForeignKey(User, related_name="msg_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="msg_receiver", on_delete=models.CASCADE)
    msg_subject = models.CharField(max_length=200, blank=True)
    msg_sent = models.DateTimeField(auto_now=True)
    msg_received = models.DateTimeField(auto_now=False, null=True, blank=True)
    msg_replied = models.DateTimeField(auto_now=False, null=True, blank=True)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Msg ID: {} |  " \
               "Sender: {} |  " \
               "Receiver: {} | " \
               "Subject: {} | " \
               "Date Created: {}".format(self.id,
                                         self.sender,
                                         self.receiver,
                                         self.msg_subject,
                                         self.msg_sent)


class MessageHistory(models.Model):
    org_message = models.ForeignKey(Message, related_name="org_message", on_delete=models.CASCADE)
    msg_next = models.ForeignKey(Message, related_name="msg_next", on_delete=models.CASCADE)

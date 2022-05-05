from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Message(models.Model):
    message_body = models.CharField(max_length=10000)
    sender = models.ForeignKey(User, related_name="msg_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="msg_receiver", on_delete=models.CASCADE)
    msg_subject = models.CharField(max_length=200, blank=True)
    msg_sent = models.DateTimeField(default=timezone.now)
    msg_received = models.DateTimeField(auto_now=False, null=True)
    msg_replied = models.DateTimeField(auto_now=False, null=True)

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
    msg_history = models.ForeignKey(Message, on_delete=models.CASCADE)

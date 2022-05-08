from django.forms import ModelForm, widgets

from message.models import Message
from item.models import Offer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MsgReplyForm(ModelForm):
    class Meta:
        model = Message
        # exclude = ['receiver', 'msg_replied', 'msg_received', 'msg_sent', 'sender']
        exclude = []
        widgets = {
            'msg_subject': widgets.TextInput(attrs={'class': 'form-control'}),
            'msg_body': widgets.Textarea(attrs={'class': 'form-control'})
        }

        def clean_msg_body(self):
            """ Cleans and validates the data before it's sent."""
            msg = self.cleaned_data["msg_body"]

            if len(msg) == 0:
                raise ValidationError(_("Message is empty"))
            return msg


class MsgItemOfferAccept(ModelForm):

    class Meta:
        model = Message
        fields = ['id']


class MsgReplyModal(ModelForm):

    class Meta:
        model = Message
        exclude = ['receiver', 'msg_replied', 'msg_received', 'msg_sent', 'sender', 'item', 'offer']
        fields =['msg_subject', 'msg_body']
        widgets = {
            'msg_subject': widgets.TextInput(attrs={'class': 'form-control'}),
            'msg_body': widgets.Textarea(attrs={'class': 'form-control'})
        }
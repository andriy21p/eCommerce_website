from django.forms import ModelForm, widgets

from message.models import Message
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MsgReplyForm(ModelForm):
    class Meta:
        model = Message
        # exclude = ['receiver', 'msg_replied', 'msg_received', 'msg_sent', 'sender']
        exclude = ['msg_received']
        widgets = {
            'msg_subject': widgets.TextInput(attrs={'class': 'form-control'}),
            'msg_body': widgets.Textarea(attrs={'class': 'form-control'})
        }
        # msg_subject = forms.CharField(label="Message Subject", max_length=200)
        # msg_body = forms.CharField(label="Text",help_text="Write your message...", max_length=500, widget=forms.Textarea)

        def clean_msg_body(self):
            """ Cleans and validates the data before it's sent."""
            msg = self.cleaned_data["msg_body"]

            if len(msg) == 0:
                raise ValidationError(_("Message is empty"))
            return msg



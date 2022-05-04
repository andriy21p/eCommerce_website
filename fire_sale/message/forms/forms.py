from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MsgReplyForm(forms.Form):
    msg_subject = forms.CharField(label="Message Subject", max_length=200)
    msg_body = forms.CharField(label="Text",help_text="Write your message...", max_length=500, widget=forms.Textarea)

    def clean_msg_body(self):
        """ Cleans and validates the data before it's sent."""
        msg = self.cleaned_data["msg_body"]

        if len(msg) == 0:
            raise ValidationError(_("Message is empty"))
        return msg



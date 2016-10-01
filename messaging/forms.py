from django import forms

from .models import Message


class NewMessageForm(forms.ModelForm):
    model = Message
    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender')
        super(NewMessageForm, self).__init__(*args, **kwargs)
        self.fields['sender'] = forms
    
    # message = forms.()
    # sender = forms.


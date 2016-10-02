from django import forms

from .models import Message, Friendship
from profiles.models import Profile


class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message',]
    
    def __init__(self, *args, **kwargs):
        super(NewMessageForm, self).__init__(*args, **kwargs)
        message = self.fields.get('message')     
        message.widget.attrs.update({
            'placeholder': 'Enter your message ...',
            'class': 'form-field textarea orange',
            'rows': 4,
            'cols': 50,
        })
        message.label = ''


class NewFriendForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter email address',
            'class': 'form-field textarea orange',
            'rows': 1,
            'cols': 50
        }
    ))

from django.contrib import admin

from .models import Contact, Conversation, Message


admin.site.register(Contact)
admin.site.register(Conversation)
admin.site.register(Message)
from django.contrib import admin

from .models import Friendship, Conversation, Message


admin.site.register(Friendship)
admin.site.register(Conversation)
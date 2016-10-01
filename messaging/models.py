from django.db import models
from django.utils import timezone

from profiles.models import Profile


class Contact(models.Model):
    profile = models.ForeignKey(Profile, related_name='my_contacts')
    contact = models.ForeignKey(Profile)

    def __str__(self):
        return '{} contact {}'.format(self.user, self.contact)


class Conversation(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user_one = models.ForeignKey(Profile, related_name='user_one')
    user_two = models.ForeignKey(Profile, related_name='user_two')
    last_message_time = models.DateTimeField()

    class Meta:
        unique_together = ('user_one', 'user_two')
        ordering = ['-last_message_time']

    def __str__(self):
        return 'Conversation between {} and {}'.format(self.user_one, self.user_two)

    def save(self, *args, **kwargs):
        if self.user_one == self.user_two:
            raise Exception('Conversation needs to be between two different users')
        super(Conversation, self).save(*args, **kwargs)

    def get_latest_message(self):
        return self.messages.latest('created_at')



class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages')
    sender = models.ForeignKey(Profile)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        message = self.message
        if len(self.message) > 10:
            message = '{}...'.format(self.message[:10])
        return message

    def save(self, *args, **kwargs):
        self.conversation.last_message_time = self.created_at
        self.conversation.save()
        super(Message, self).save(*args, **kwargs)

    def set_to_seen(self):
        self.seen = True
        self.save()

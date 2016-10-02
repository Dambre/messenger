from django.db import models
from django.utils import timezone
from django.core.exceptions import FieldError

from profiles.models import Profile


class Friendship(models.Model):
    user = models.ForeignKey(Profile, related_name='friends')
    friend = models.ForeignKey(Profile)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return "{} is {}'s friend".format(self.friend, self.user)

    def save(self, *args, **kwargs):
        if self.user == self.friend:
            raise FieldError('Friendship can\'t be created between same user.')
        
        adding = False
        if self._state.adding:
            adding = True

        super(Friendship, self).save(*args, **kwargs)
        if adding:
            Friendship.objects.get_or_create(user=self.friend, friend=self.user)


class Conversation(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user_one = models.ForeignKey(Profile, related_name='user_one')
    user_two = models.ForeignKey(Profile, related_name='user_two')
    last_message_time = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('user_one', 'user_two')
        ordering = ['-last_message_time']

    def __str__(self):
        return 'Conversation between {} and {}'.format(self.user_one, self.user_two)

    def save(self, *args, **kwargs):
        if self.user_one == self.user_two:
            raise FieldError('Conversation needs to be between two different users')
        super(Conversation, self).save(*args, **kwargs)

    def get_latest_message(self):
        try:
            return self.messages.latest('created_at')
        except Message.DoesNotExist:
            return None

    @property
    def senders(self):
        return [self.user_one, self.user_two]


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
        if self._state.adding:
            if self.sender not in self.conversation.senders:
                raise FieldError('Invalid sender')
            self.conversation.last_message_time = self.created_at
            self.conversation.save()
        super(Message, self).save(*args, **kwargs)
    

    def set_to_seen(self):
        self.seen = True
        self.save()

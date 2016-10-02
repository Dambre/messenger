
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Conversation, Friendship
from .forms import NewFriendForm, NewMessageForm
from profiles.models import Profile

class IsLoggedInMixin(LoginRequiredMixin):
    login_url = reverse_lazy('profiles:login')


class AuthorizedToConversationMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(user_one=user) | Q(user_two=user),
            id=self.kwargs['conversation'],
            ).exists()


class GetAllConversationsView(IsLoggedInMixin, View):
    def get(self, request):
        user = request.user
        _conversations = Conversation.objects.filter(
            Q(user_one=user) | Q(user_two=user))
        
        conversations = list()
        for _con in _conversations:
            latest_message = _con.get_latest_message()
            message = ''
            
            senders = filter(
                lambda x: False if x.email == user.email else True, _con.senders)
            senders = [sender.name for sender in senders]

            seen = True
            if latest_message:
                seen = latest_message.seen
                if latest_message.sender == user:
                    seen = True
                message = latest_message.message
            conversations.append({
                'url': reverse_lazy(
                    'conversation', kwargs={
                        'conversation': _con.id}),
                'senders': ', '.join(senders),
                'last_message': message,
                'seen': seen,
                'reply_url': reverse_lazy(
                    'new_message', kwargs={
                        'conversation': _con.id}),
            })
        return render(
            request, 'messaging/conversations.html', {
                'conversations': conversations,
                'back_url': reverse_lazy('messages')})


class GetConversationView(IsLoggedInMixin, AuthorizedToConversationMixin, View):
    def get(self, request, conversation):
        conversation_obj = get_object_or_404(Conversation, id=conversation)
        user = self.request.user
        _messages = conversation_obj.messages.all()
        messages = []
        recipients = filter(
                lambda x: False if x.email == self.request.user.email else True,
                conversation_obj.senders)
        recipients = [_rec.name for _rec in recipients]
        for message in _messages:
            if message.sender == user:
                seen = True
            
            else:
                seen = message.seen
                if not seen:
                    message.set_to_seen()

            messages.append({
                'message': message.message,
                'seen': seen,
                'sender': message.sender
            })

        return render(
            request, 'messaging/messages.html', {
            'messages': messages,
            'back_url': reverse_lazy('messages'),
            'recipient': ', '.join(recipients)
        })


class NewMessageView(IsLoggedInMixin, AuthorizedToConversationMixin, View):
    template_name = 'messaging/new_message.html'
    form = NewMessageForm

    def get(self, request, conversation):
        conversation_obj = get_object_or_404(Conversation, id=conversation)
        recipients = filter(
                lambda x: False if x.email == self.request.user.email else True,
                conversation_obj.senders)
        recipients = [_rec.name for _rec in recipients]
        return render(
            request, self.template_name, {
                'form': self.form(),
                'new_message_url': reverse_lazy(
                    'new_message',
                    kwargs={'conversation': conversation}),
                'recipient': ', '.join(recipients),
                'back_url': reverse_lazy('messages')
            })

    def post(self, request, conversation):
        conversation_obj = get_object_or_404(Conversation, id=conversation)
        form = self.form(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = self.request.user
            message.conversation = conversation_obj
            message.save()
            return redirect(
                reverse_lazy(
                    'conversation',
                    kwargs={'conversation': conversation}
                )
            )
        return render(request, self.template_name, {'form': form})


class FriendsView(IsLoggedInMixin, TemplateView):
    http_method_names = ['get',]
    template_name = 'messaging/friends.html' 

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        user = self.request.user
        _friends = Friendship.objects.filter(
            user=user).order_by('friend__email').select_related('friend')
        
        friends = list()
        for _friend in _friends:
            friend = _friend.friend
            try:
                conversation = Conversation.objects.get(
                    Q(user_one=user, user_two=friend) | Q(user_one=friend, user_two=user)
                )
            
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create(user_one=user, user_two=friend)
            
            friends.append({
                'name': friend.name,
                'conversation': reverse_lazy(
                    'new_message',
                    kwargs={'conversation': conversation.id}),
                'delete_url': reverse_lazy(
                    'delete_friend',
                    kwargs={'friend_id': friend.id})
            })
        context['friends'] = sorted(friends, key=lambda x: x['name'])
        return context


class NewFriendView(IsLoggedInMixin, View):
    template_name = 'messaging/new_friend.html'
    form = NewFriendForm

    def get(self, request):
        return render(
            request, self.template_name, {'form': self.form()}
        )

    def post(self, request):
        form = self.form(self.request.POST)
        if form.is_valid():
            try:
                profile = Profile.objects.get(email=form.cleaned_data['email'])
            except Profile.DoesNotExist:
                return render(
                    request, self.template_name, {
                        'form': self.form(),
                        'error': 'User Does not exist'})
            friendship, created = Friendship.objects.get_or_create(
                user=request.user, friend=profile)
            if not created:
                return render(
                    request, self.template_name, {
                        'form': self.form(),
                        'error': 'You already have this friend added'
                    })
            return redirect(reverse_lazy('friends'))
        
        return render(
            request, self.template_name, {'form': form})


class DeleteFriendView(IsLoggedInMixin, View):
    def get(self, request, friend_id):
        friend = get_object_or_404(Profile, id=friend_id)
        friendship1 = get_object_or_404(
            Friendship, user=request.user, friend=friend)

        friendship2 = get_object_or_404(
            Friendship, user=friend, friend=request.user)
        
        with transaction.atomic():
            friendship1.delete()
            friendship2.delete()
        return redirect(reverse_lazy('friends'))

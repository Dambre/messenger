from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .models import Conversation, Contact


class IsLoggedInMixin(LoginRequiredMixin):
    login_url = reverse_lazy('profiles:login')
    redirect_field_name = '/messages'


class AuthorizedToConversationMixin(UserPassesTestMixin):
    def test_func(self):
        method = self.request.method
        if method == 'GET':
            user = self.request.user
            return Conversation.objects.filter(
                Q(user_one=user) | Q(user_two=user),
                id=self.request.GET['conversation'],
                ).exists()
        
        elif method == 'POST':
            user = self.request.user
            return Conversation.objects.filter(
                Q(user_one=user) | Q(user_two=user),
                id=self.request.POST.get('conversation'),
                ).exists()
        
        return False


class GetAllConversationsView(IsLoggedInMixin, View):
    def get(self, request):
        user = request.user
        conversations = Conversation.objects.filter(
            Q(user_one=user) | Q(user_two=user))
        
        return render(
            request, 'messaging/conversations.html',
            {'conversations': conversations})


class GetConversationView(IsLoggedInMixin, AuthorizedToConversationMixin, View):
    def get(self, request, conversation):
        return HttpResponse(Coversation.objects.get(id=conversation))


class SendMessageView(IsLoggedInMixin, AuthorizedToConversationMixin, TemplateView):
    def get(self, request, contact):
        contact = Contact.objects.get(email=contact)
        form = MessageForm()
        

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(sender=request.user, conversation=request.POST.get('conversation')) # pabaigti redirect kai success
#TODO 
        # pabaigti redirect kai fail


def send_message(request):
    conversation = Conversation.objects.get_or_create(
        Q(user_one=request.user, user_two=friend) | Q(user_one=friend, user_two=request.user))
    # message = Message.objects.create(
    #     sender=request.user, message.)

    return HttpResponse('New Message Created')

class ContactsView(IsLoggedInMixin, TemplateView):
    http_method_names = ['get',]
    template_name = 'contacts.html' 
    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        context['contacts'] = Contact.objects.filter(
            profile=request.user).order_by('contact__email')
        return context

class NewContact(IsLoggedInMixin, TemplateView):
    http_method_names = ['post',]
    template_name = 'new_contact.html'
    
    def POST(self, request, contact):
        # Contact.objects.get_or_create(email=)
        pass
        
# class based viewsa padaryt
        return HttpResponse('New Contact Created')

#TODO
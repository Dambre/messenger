from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='messages')),
    url(r'^messages$', views.GetAllConversationsView.as_view(), name='messages'),
    url(r'^messages/(?P<conversation>\d+)$', views.GetConversationView.as_view(), name='coversation_by_id'),
    url(r'^contacts$', views.ContactsView.as_view(), name='contacts'),
    url(r'^add_contact$', views.NewContact.as_view(), name='add_contact')
]
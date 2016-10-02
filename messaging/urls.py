from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='messages')),
    
    url(r'^messages$', views.GetAllConversationsView.as_view(), name='messages'),
    url(r'^messages/(?P<conversation>\d+)$', views.GetConversationView.as_view(), name='conversation'),
    url(r'^messages/(?P<conversation>\d+)/new_message$', views.NewMessageView.as_view(), name='new_message'),

    url(r'^friends$', views.FriendsView.as_view(), name='friends'),
    url(r'^new_friend$', views.NewFriendView.as_view(), name='new_friend'),
    url(r'^delete_friend/(?P<friend_id>\d+)$', views.DeleteFriendView.as_view(), name='delete_friend'),
]
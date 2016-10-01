from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^signup$', views.RegisterView.as_view(), name='signup'),
    url(r'^logout$', views.logout_view, name='logout'),
]
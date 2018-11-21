
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import TemplateView


from .views import *


urlpatterns = [
    url(r'^register/$', register_page, name='register'),
    url(r'^login/$', login_page, name='login'),
    url(r'^logout/$',logout_page, name='logout'),
    url(r'^activate_page/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate_page, name='activate_page'),
    url(r'^profile/$',profile_page, name='profile_page'),
    url(r'^notification/$',show_my_notifications, name='notification'),
    url(r'^edit_profile_page/$',edit_profile_page, name='edit_profile'),
    url(r'^password/$',change_password, name='change_password'),

]

from django.conf.urls import include, url

from .views import SearchAuctionView, advanced_search
from . import views

urlpatterns = [

    url(r'^$',SearchAuctionView.as_view(), name='search'),
    url(r'^advanced_search/$',views.advanced_search, name='advanced_search'),


]


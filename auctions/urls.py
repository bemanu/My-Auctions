from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^$', AuctionListView.as_view(), name='list'),
    url(r'^detail/(?P<auction_id>[0-9]+)/$', auction_detail_view, name='detail'),

    url(r'^wall/$', upcoming_auctions_view, name='wall'),
    url(r'^create_auction/$', create_auction, name='create_auction'),
    url(r'^partecipated_auction/$',partecipated_auction, name= 'partecipated_auction'),
    url(r'^m_auction/$',mine_auction, name='m_auction'),
    url(r'^delete/(?P<auction_view>[0-9]+)/$', delete_auction, name='delete'),
    url(r'^chart/$', get_data, name='stat'),
    url(r'^chart_data/$',get_view_data, name='stats'),
]


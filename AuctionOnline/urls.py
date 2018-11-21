from django.contrib import admin
from . import views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from .views import home_page




urlpatterns = [
    url(r'^$',home_page, name='home'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^auctions/', include('auctions.urls', namespace="auctions")),
    url(r'^search/', include('search.urls', namespace ="search")),

    url(r'^admin/', include(admin.site.urls)),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

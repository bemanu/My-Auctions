from django.contrib import admin

from .models import Auction, Notify


class AuctionAdmin(admin.ModelAdmin):

    fields = [
        'title',
        'category',
        'image',
        'description',
        'min_price',
        'deadline',
        'active',
    ]

    list_display = [
        'title',
        'category',
        'min_price',
        'offer',
        'deadline',
        'check_deadline',
        'active',
        'vendor',
    ]


class NotifyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'auction',
        'time',
    ]


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Notify, NotifyAdmin)




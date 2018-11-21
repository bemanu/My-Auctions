from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user',  ]
    fields = [
        'user',
        'email_confirmed',
        'bio',
        'birth_date',
        'address',
        'mine_auctions']


admin.site.register(Profile, ProfileAdmin)




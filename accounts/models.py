
from django.contrib.auth.models import User
from django.db import models
from auctions.models import Auction, Notify

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(blank=True, max_length=300)
    birth_date = models.DateField(null=True, max_length=125)
    address = models.CharField(blank=True, null=True, max_length=125)
    mine_auctions = models.ManyToManyField(Auction)

    @property
    def __unicode__(self):
        return '%s' % self.user.username

    @property
    def show_messages(self):
        note = Notify.objects.filter(user=User.objects.get(pk=self.user.id))
        return note

    def get_my_auction(self):
        return self.mine_auctions


@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

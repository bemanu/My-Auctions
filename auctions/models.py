
import os
import random
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

TIME_LIMIT = 3


CATEGORY = [
    ('comics', 'Comics'),
    ('computer parts', 'Computer Parts'),
    ('collections', 'Collection'),
    ('others', 'Others'),

]


#
# AUCTION_TYPE = [
#     ('free bid', 'Free Bid'),
#     ('fixed bid', 'Fixed Bid'),
# ]


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.split(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "auction/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class AuctionQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) )

        return self.filter(lookups).distinct()

    def exclude (self,to_b):
        return self.exclude(to_b)


def bid(obj, offer, profile):
    obj.offer = offer
    obj.high_bidder = profile.user.username
    if not obj in profile.mine_auctions.all():
        profile.mine_auctions.add(obj)
        profile.save()
    return obj


class AuctionManager(models.Manager):
    def get_queryset(self):
        return AuctionQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def minus(self,to_b):
        return self.get_queryset().exclude(to_b)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query).filter(active=True)

    # def minimum_bid(self, base):
    #     outbid=0
    #     if Auction.auction_type == 'fixed bid':
    #         outbid = 1
    #         if self is None:
    #             outbid= 1
    #         elif 10 < base < 99:
    #             outbid = ((base * 3) / 100)
    #         elif 100 < base < 999:
    #             outbid = ((base * 5) / 100)
    #         elif base > 1000:
    #             outbid = (base * 10) / 100
    #     else:
    #         if 10 < base < 30:
    #             outbid = 3
    #         elif 30 < base < 100:
    #             outbid = 5
    #         elif base > 100:
    #             outbid = 10
    #
    #     return outbid

    def time_left(self):
        diff = (self.deadline - datetime.now())
        return timedelta.total_seconds(diff)

    def divid_by_cate(self):
        dictionary = list()
        for q in CATEGORY:
            dictionary.append({q[0]: self.all().filter(category=q[0])})
        return dictionary

    def notify(self, auction):
        if not auction.high_bidder == '':
            user = User.objects.get(username=str(auction.high_bidder))
            note = Notify(user=user, auction=auction)

            note.save()

    def update_deadline(self):
        tob_checked = Auction.objects.filter(active=True)
        for q in tob_checked:
            if timezone.now() >= q.deadline:
                q.active = False
                self.notify(q)
                q.save()


    def deadline_filter(self, ris,expire_at):
        now = timezone.now()
        minim = now
        maxim = now + timedelta(hours=(int(expire_at)))
        risult = ris.filter(deadline__gt=minim).filter(deadline__lt=maxim)
        # print (risult)
        return risult



class Auction(models.Model):
    title = models.CharField(max_length=45)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    min_price = models.DecimalField(default="0.00", help_text="in Euro.", max_digits=5, decimal_places=2)
    offer = models.DecimalField(help_text="in Euro.", max_digits=5, decimal_places=2, null=True)
    description = models.TextField(max_length=300, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY)
    vendor = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    high_bidder = models.CharField(max_length=15, null=True, default="")
    # auction_type = models.CharField(max_length=25, choices=AUCTION_TYPE, default='Free Bid')
    active = models.BooleanField(default=True)

    objects = AuctionManager()

    def get_absolute_url(self):
        return reverse("auctions:detail", args=[self.pk])

    @property
    def __unicode__(self):
        return self.title

    def check_deadline(self):
        return self.deadline - timedelta(hours=TIME_LIMIT) <= timezone.now() <= self.deadline

    check_deadline.admin_order_field = 'deadline'
    check_deadline.boolean = True
    check_deadline.short_description = 'Is expired?'


class Notify(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    auction = models.ForeignKey(Auction)
    send_mail(
        'Auction Ended',
        'aucti',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )

    def __unicode__(self):
        return self.id


from django.test import TestCase
from django.urls import reverse

from .models import Auction
from django.utils import timezone
import datetime

'''controlling the state of deadline of the auction to see whether they are tru or false'''


class AuctionModelTests(TestCase):
    def deadline_control_test(self):
        expired = timezone.now() - datetime.timedelta(hours=1)
        almost_expired = timezone.now() + datetime.timedelta(hours=1)
        tb_expired = timezone.now() + datetime.timedelta(hours=5)

        expired_auction = Auction(deadline=expired)
        almst_expired_auction = Auction(deadline=almost_expired)
        tb_expired_auction = Auction(deadline=tb_expired)

        self.assertEqual(expired_auction.check_deadline(), False)
        self.assertEqual(almst_expired_auction.check_deadline(), True)
        self.assertEqual(tb_expired_auction.check_deadline(), False)


class AuctionTests(TestCase):

    def setUp(self):
        Auction.objects.create(title='brick', description="this is just a brick", min_price=15,
                               deadline='2018-12-12 11:00')

    def test_auction_view(self):
        response = self.client.get(reverse('auctions:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/list.html')

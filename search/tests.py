from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

''' controlling if an unauthorized user can access pages that they shouldnt have the 
    privilege to access.
    and that if they are non authorized the page they are redirected is correct.
'''


class AuctionViewTests(TestCase):
    def set_up(self):
        user = User.objects.create_user('tmp', 'temporary@gmail.com', 'tmmmppprry')
        user.is_active= True

    def test_user_not_login(self):
        path = '/search/advanced_search/'
        redir = '/accounts/login/'+'?next='+path
        client = Client()
        response = client.get(path)
        self.assertRedirects(response, redir)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)


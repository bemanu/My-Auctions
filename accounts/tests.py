# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.test.client import Client
#
#
# class AuctionViewTests(TestCase):
#     def set_up(self):
#         user = User.objects.create_user('tmp1', 'temporary1@gmail.com', 'tmmmppprry1')
#         user.is_active=True
#
#
#     def test_login_section(self):
#         client = Client()
#         client.post('/accounts/login/', {'username': 'tmp1', 'password': 'tmmmppprry1'})
#
#         response = client.get('auctions/wall')
#         print('This is response ', response)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, '/auctions/wall.html')
#
#

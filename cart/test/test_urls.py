from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.

class TestUrls(TestCase):

    def setUp(self):
        # self.cart_url = self.client.get(reverse('cart:cart'))
        # self.add_to_cart_url = self.client.get(reverse('cart:cart'))
        # self.add_to_cart_url = self.client.get(reverse('cart:add-to-cart'))
        self.checkout_url = self.client.get(reverse('cart:checkout'))


    def test_urls(self):
        # self.assertEqual(self.cart_url.status_code, 200)
        # self.assertEqual(self.add_to_cart_url.status_code, 200)
        self.assertTrue(self.checkout_url.resolver_match.route == 'action/checkout/')
        self.assertTrue(self.checkout_url.resolver_match.url_name == 'checkout' )
        self.assertEqual(self.checkout_url.status_code, 200)
from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse
from marketplace.models import Listing, Career
from django.utils import timezone

from mixins.init_accounts import InitAccountsMixin


class ApplicationsTestCase(TestCase, InitAccountsMixin):
    @classmethod
    def setUpTestData(cls):
        super().set_up()
        cls.rand_employer = cls.create_new_employer()
        cls.listing = cls.create_listing(cls)

    def login(self, profile) -> None:
        self.client.login(username=profile.email, password=self.password)

    def logout(self) -> None:
        self.client.logout()

    @staticmethod
    def listing_data():
        return {
            
        }

    def check_login_redirected(self, path):
        response = self.client.get(path, follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def test_create_listing(self):
        response = self.client.post(reverse('createlisting'))
from typing import Dict, List
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
        cls.listing_id = 0
        cls.career = Career.objects.create(career='some career')
        cls.career.save()

    @staticmethod
    def find_listing(listing_id) -> Listing:
        return Listing.objects.get(id=listing_id)
        

    def create_listing(self, data) -> HttpResponse:
        resp = self.client.post(reverse('createlisting'), data=data, follow=True)
        self.listing_id += 1
        return resp

    def login(self, profile) -> None:
        self.client.login(username=profile.email, password=self.password)

    def logout(self) -> None:
        self.client.logout()

    def listing_data(self) -> Dict:
        return {
            'id': self.listing_id,
            'company': self.employer,
            'title': 'some listing',
            'type': 'Unpaid',
            'where': 'Virtual',
            'career': self.career.id,
            'application_deadline': timezone.now(),
            'time_commitment': 'lots',
            'description': 'description'
        }

    def check_login_redirected(self, path):
        response = self.client.get(path, follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def test_create_listing(self):
        self.login(self.employer)
        response = self.create_listing(self.listing_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.find_listing(self.listing_id))

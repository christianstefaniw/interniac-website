from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from mixins.init_accounts import InitAccountsMixin
from marketplace.models import Listing, Career


class ApplicationsTestCase(TestCase, InitAccountsMixin):
    @classmethod
    def setUpTestData(cls):
        super().set_up()
        cls.listing_id = 1
        cls.listing_slug = 'some-listing'
        cls.career = Career.objects.create(career='some career')
        cls.career.save()

    @staticmethod
    def find_listing(listing_id) -> Listing:
        return Listing.objects.get(id=listing_id)
        
    def create_new_career(self) -> Career:
        return Career.objects.create(career='rand career')

    def create_listing(self, data) -> HttpResponse:
        return self.client.post(reverse('createlisting'), data=data, follow=True)

    def update_listing(self, data) -> HttpResponse:
        return self.client.post(reverse('edit_listing', kwargs={'slug': self.listing_slug}), data=data, follow=True)

    def login(self, profile) -> None:
        self.client.login(username=profile.email, password=self.password)

    def logout(self) -> None:
        self.client.logout()

    @property
    def listing_data(self) -> dict:
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

    def test_create_listing(self):
        self.login(self.employer)
        data = self.listing_data
        response = self.create_listing(data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.find_listing(self.listing_id))

    def test_create_paid_listing(self):
        self.login(self.employer)
        data = self.listing_data
        data['type'] = 'Paid'
        data['pay'] = '$12'
        response = self.create_listing(data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.find_listing(self.listing_id))

    def test_create_in_person_listing(self):
        self.login(self.employer)
        data = self.listing_data
        data['where'] = 'In-Person'
        data['location'] = 'somewhere'
        response = self.create_listing(data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.find_listing(self.listing_id))

    def test_create_listing_with_new_career(self):
        self.login(self.employer)
        data = self.listing_data
        data['career'] = ''
        data['new_career'] = 'new career'
        response = self.create_listing(data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.find_listing(self.listing_id))

    def test_create_listing_paid_with_no_pay(self):
        self.login(self.employer)
        data = self.listing_data
        data['type'] = 'Paid'
        response = self.create_listing(data)
        self.assertTrue(response.context['form'].errors['pay'])

    def test_create_listing_in_person_with_no_location(self):
        self.login(self.employer)
        data = self.listing_data
        data['where'] = 'In-Person'
        response = self.create_listing(data)
        self.assertTrue(response.context['form'].errors['location'])
    
    def test_create_listing_with_no_career(self):
        self.login(self.employer)
        data = self.listing_data
        data['career'] = ''
        response = self.create_listing(data)
        self.assertTrue(response.context['form'].errors['career'])

    def test_create_listing_unpaid_with_pay(self):
        self.login(self.employer)
        data = self.listing_data
        data['pay'] = '5'
        self.create_listing(data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertEqual(listing.pay, '')

    def test_create_listing_virtual_with_location(self):
        self.login(self.employer)
        data = self.listing_data
        data['where'] = 'Virtual'
        data['location'] = 'location'
        self.create_listing(data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertEqual(listing.location, '')

    def test_create_listing_with_career_and_new_career(self):
        self.login(self.employer)
        data = self.listing_data
        data['new_career'] = 'new'
        self.create_listing(data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertEqual(listing.career, self.career)

    def test_delete_listing(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        response = self.client.post(reverse('delete_listing', kwargs={'listing_id': self.listing_id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(Listing.DoesNotExist, Listing.objects.get, id=self.listing_id)

    def test_update_listing(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        response = self.update_listing(self.listing_data)
        self.assertTrue(response.status_code, 200)

    def test_update_listing_paid(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['type'] = 'Paid'
        update_data['pay'] = '$10'
        self.update_listing(update_data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertTrue(listing.type == 'Paid')
        self.assertTrue(listing.pay == '$10')

    def test_update_listing_paid_with_no_pay(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['type'] = 'Paid'
        update_data['pay'] = ''
        response = self.update_listing(update_data)
        self.assertTrue(response.context['form'].errors['pay'])

    def test_update_listing_in_person(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['where'] = 'In-Person'
        update_data['location'] = 'somewhere'
        self.update_listing(update_data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertTrue(listing.where == 'In-Person')
        self.assertTrue(listing.location == 'somewhere')

    def test_update_listing_in_person_with_no_location(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['where'] = 'In-Person'
        update_data['location'] = ''
        response = self.update_listing(update_data)
        self.assertTrue(response.context['form'].errors['location'])
    
    def test_update_listing_with_brand_new_career(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['career'] = ''
        update_data['new_career'] = 'new career'
        self.update_listing(update_data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertTrue(listing.career.career == 'new career')

    def test_update_listing_with_new_career(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        new_career = self.create_new_career()
        update_data = self.listing_data
        update_data['career'] = new_career.id
        self.update_listing(update_data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertTrue(listing.career == new_career)

    def test_update_listing_virtual_with_location(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['location'] = 'location'
        self.update_listing(update_data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertTrue(listing.location == '')

    def test_update_listing_unpaid_with_pay(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['pay'] = '5'
        self.update_listing(update_data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertTrue(listing.pay == '')

    def test_update_listing_new_career_and_brand_new_career(self):
        self.login(self.employer)
        self.create_listing(self.listing_data)
        update_data = self.listing_data
        update_data['new_career'] = 'new career'
        self.update_listing(update_data)
        listing = Listing.objects.get(id=self.listing_id)
        self.assertTrue(listing.career == self.career)

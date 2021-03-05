from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.urls import reverse

from marketplace.models import Listing, Career
from test_mixins.init_accounts_for_tests import InitAccountsMixin


class ApplicationsTestCase(TestCase, InitAccountsMixin):

    @classmethod
    def setUpTestData(cls):
        super(ApplicationsTestCase, cls).set_up()
        cls.listing = cls.create_listing()

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def login(self, profile) -> None:
        self.client.login(username=profile.email, password=self.password)

    @classmethod
    def create_listing(cls) -> Listing:
        career = Career.objects.create(career='some career')
        career.save()
        return Listing.objects.create(company=cls.employer, title='some listing', type='Unpaid', where='Virtual',
                                      career=career, application_deadline=timezone.now(), description='description')

    def check_login_redirected(self, path):
        response = self.client.get(path, follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def test_student_apply(self):
        self.check_login_redirected(reverse('apply', kwargs={'listing_id': self.listing.id}))
        self.login(self.student)
        response = self.client.get(reverse('apply', kwargs={'listing_id': self.listing.id}),
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.listing.applications.get(id=self.student.id))

    def test_employer_apply(self):
        self.check_login_redirected(reverse('apply', kwargs={'listing_id': self.listing.id}))
        self.login(self.employer)
        self.assertRaises(PermissionError, self.client.get, reverse('apply', kwargs={'listing_id': self.listing.id}),
                          follow=True)

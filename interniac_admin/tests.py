from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from mixins.init_accounts import InitAccountsMixin
from marketplace.models import Listing, Career
from accounts.models import User


class ApplicationsTestCase(TestCase, InitAccountsMixin):
    @classmethod
    def setUpTestData(cls):
        super().set_up()
        cls.admin = User.objects.create_superuser(email='admin@gmail.com', first_name='first', last_name='last',
                                                  password='password',
                                                  )

    def login(self, profile) -> None:
        self.client.login(username=profile.email, password=self.password)

    def logout(self) -> None:
        self.client.logout()

    def create_career_info(self) -> HttpResponse:
        data = {
            'content': 'content'
        }
        return self.client.post(
            reverse('create_career_info'), data=data, follow=True)

    def test_create_career(self):
        response = self.create_career_info()
        self.assertEqual(403, response.status_code)
        self.logout()
        self.login(self.admin)
        response = self.create_career_info()
        self.assertEqual(200, response.status_code)

    def test_view_all_users(self):
        self.login(self.student)
        response = self.client.get(
            reverse('all_users'))
        self.assertEqual(403, response.status_code)
        self.logout()
        self.login(self.employer)
        response = self.client.get(
            reverse('all_users'))
        self.assertEqual(403, response.status_code)

    def test_view_single_user(self):
        self.login(self.student)
        response = self.client.get(
            reverse('user_info', args=[self.employer.slug]))
        self.assertEqual(403, response.status_code)
        self.logout()
        self.login(self.employer)
        response = self.client.get(
            reverse('user_info', args=[self.student.slug]))
        self.assertEqual(403, response.status_code)

    def test_delete_user(self):
        self.login(self.student)
        response = self.client.post(
            reverse('delete_account', kwargs={'id': self.employer.id}))
        self.assertEqual(403, response.status_code)
        self.logout()
        self.login(self.employer)
        response = self.client.post(
            reverse('delete_account', kwargs={'id': self.student.id}))
        self.assertEqual(403, response.status_code)
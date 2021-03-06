from django.http import HttpResponse
from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User
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

    def logout(self) -> None:
        self.client.logout()

    def apply(self) -> HttpResponse:
        return self.client.get(reverse('apply', kwargs={'listing_id': self.listing.id}),
                               follow=True)

    @classmethod
    def create_listing(cls) -> Listing:
        career = Career.objects.create(career='some career')
        career.save()
        return Listing.objects.create(company=cls.employer, title='some listing', type='Unpaid', where='Virtual',
                                      career=career, application_deadline=timezone.now(), description='description')

    def check_login_redirected(self, path):
        response = self.client.get(path, follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def login_apply_out(self):
        self.login(self.student)
        self.apply()
        self.logout()

    def test_random_employer_request_interview(self):
        new_employer = User.objects.create_user(email='rand@gmail.com', first_name='first', last_name='last',
                                                password='password',
                                                is_student=False, is_employer=True)
        new_employer.save()
        self.login(new_employer)
        self.assertRaises(PermissionError, self.client.get, reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_employer_request_interview(self):
        self.login_apply_out()
        self.check_login_redirected(reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))
        self.login(self.employer)
        response = self.client.get(reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student in self.listing.applications.all())
        self.assertTrue(self.student in self.listing.interview_requests.all())

    def test_student_request_interview(self):
        self.login_apply_out()
        self.check_login_redirected(reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))
        self.login(self.student)
        self.assertRaises(PermissionError, self.client.get, reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_employer_reject(self):
        self.login_apply_out()
        self.check_login_redirected(reverse('reject', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))
        self.login(self.employer)
        response = self.client.get(reverse('reject', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.listing.applications.all())
        self.assertTrue(self.student in self.listing.rejections.all())
        self.listing.rejections.remove(self.student)

    # try to reject a student as a student
    def test_student_reject(self):
        self.login_apply_out()
        self.check_login_redirected(reverse('reject', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))
        self.login(self.student)
        self.assertRaises(PermissionError, self.client.get, reverse('reject', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_employer_accept(self):
        self.login_apply_out()
        self.check_login_redirected(reverse('accept',
                                            kwargs={
                                                'listing_id': self.listing.id,
                                                'student_id': self.student.id
                                            }))
        self.login(self.employer)
        response = self.client.get(reverse('accept',
                                           kwargs={
                                               'listing_id': self.listing.id,
                                               'student_id': self.student.id
                                           }), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student in self.listing.acceptances.all())
        self.assertFalse(self.student in self.listing.applications.all())
        self.listing.acceptances.remove(self.student)

    # try to accept a student as a student
    def test_student_accept(self):
        self.login_apply_out()
        self.login(self.student)
        self.assertRaises(PermissionError, self.client.get, reverse('accept',
                                                                    kwargs={
                                                                        'listing_id': self.listing.id,
                                                                        'student_id': self.student.id
                                                                    }))

    def test_student_unapply(self):
        self.check_login_redirected(reverse('unapply', kwargs={'listing_id': self.listing.id}))
        self.login(self.student)
        self.apply()
        response = self.client.get(reverse('unapply', kwargs={'listing_id': self.listing.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, self.listing.applications.get, id=self.student.id)

    def test_employer_unapply(self):
        self.check_login_redirected(reverse('unapply', kwargs={'listing_id': self.listing.id}))
        self.login(self.employer)
        self.assertRaises(PermissionError, self.client.get, reverse('unapply', kwargs={'listing_id': self.listing.id}),
                          follow=True)

    def test_student_apply(self):
        self.check_login_redirected(reverse('apply', kwargs={'listing_id': self.listing.id}))
        self.login(self.student)
        response = self.apply()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.listing.applications.get(id=self.student.id))

    def test_employer_apply(self):
        self.check_login_redirected(reverse('apply', kwargs={'listing_id': self.listing.id}))
        self.login(self.employer)
        self.assertRaises(PermissionError, self.client.get, reverse('apply', kwargs={'listing_id': self.listing.id}),
                          follow=True)

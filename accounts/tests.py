from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, RequestFactory
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

from test_mixins.init_accounts_for_tests import InitAccountsMixin
from .models import *


class UserTestCase(TestCase, InitAccountsMixin):

    @classmethod
    def setUpTestData(cls):
        super(UserTestCase, cls).set_up()

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def login(self, profile):
        self.client.login(username=profile.email, password=self.password)

    def check_login_redirected(self, path):
        response = self.client.get(path, follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def test_unique_student_phone(self):
        new_student = User.objects.create_user(email='email@gmail.com', first_name='first',
                                               last_name='last',
                                               password='password',
                                               is_student=True, is_employer=False)

        self.assertRaises(ValidationError, super(UserTestCase, self).student_profile, new_student.id, self.student.profile.phone)

    def test_unique_email(self):
        self.assertRaises(IntegrityError, User.objects.create_user, email=self.student.email, first_name='first',
                          last_name='last',
                          password='password',
                          is_student=True, is_employer=False)

    def test_unique_slug(self):
        new_student = User.objects.create_user(email='email@gmail.com', first_name='first', last_name='last',
                                               password='password',
                                               is_student=True, is_employer=False)
        super(UserTestCase, self).student_profile(new_student.id, '+12125552369')
        new_student.slug_student()
        self.assertNotEqual(self.student.slug, new_student.slug)

    def test_existing_email(self):
        self.assertRaises(IntegrityError, User.objects.create_user, email='test@gmail.com', first_name='first',
                          last_name='last',
                          password='password',
                          is_student=True, is_employer=False)

    def test_delete_employer_url(self):
        user_instance = User.objects.get(email=self.employer_email)
        self.assertTrue(user_instance)

        self.check_login_redirected(reverse('delete'))
        self.login(user_instance)

        response = self.client.get(reverse('delete'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, User.objects.get, email=self.employer_email)

    def test_delete_student_url(self):
        user_instance = User.objects.get(email=self.student_email)

        self.check_login_redirected(reverse('delete'))
        self.login(user_instance)
        self.assertTrue(user_instance)
        response = self.client.get(reverse('delete'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, User.objects.get, email=self.student_email)

    def test_listings_employer_url(self):
        self.check_login_redirected(reverse('listings'))
        self.login(self.employer)
        response = self.client.get(reverse('listings'), follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('listings'))
        self.assertEqual(response.status_code, 200)

    def test_listings_student_url(self):
        self.check_login_redirected(reverse('listings'))
        self.login(self.student)
        self.assertRaises(PermissionError, self.client.get, reverse('listings'))

    def test_profile_employer_url(self):
        self.check_login_redirected(reverse('profile'))
        self.login(self.employer)
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].email, self.employer.email)

    def test_profile_student_url(self):
        self.check_login_redirected(reverse('profile'))
        self.login(self.student)
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].email, self.student.email)

    def test_employer_company_website(self):
        old_site = self.employer.employer_profile.company_website
        self.assertEqual(self.employer.employer_profile.company_website, 'http://www.google.com')
        self.employer.employer_profile.company_website = 'not a website'
        self.assertRaises(ValidationError, self.employer.employer_profile.full_clean)
        self.employer.employer_profile.company_website = old_site

    def test_employer_company_name(self):
        self.assertEqual(self.employer.employer_profile.company_name, 'some company')

    def test_employer_profile_attached(self):
        self.assertTrue(self.employer.employer_profile)

    def test_employer_first_name(self):
        self.assertEqual(self.employer.first_name, 'first')

    def test_employer_last_name(self):
        self.assertEqual(self.employer.first_name, 'first')

    def test_employer_is_student(self):
        self.assertEqual(self.employer.is_student, False)

    def test_employer_is_employer(self):
        self.assertEqual(self.employer.is_employer, True)

    def test_employer_profile_picture(self):
        self.assertEqual(self.employer.profile_picture.name, 'profile_pictures/default.png')

    def test_expected_employer_str(self):
        expected = self.employer.employer_profile.company_name
        self.assertEqual(str(self.employer), expected)

    def test_student_link_4(self):
        old_link = self.student.profile.link4
        self.assertEqual(self.student.profile.link4, None)
        self.student.profile.link4 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link4 = old_link

    def test_student_link_3(self):
        old_link = self.student.profile.link3
        self.assertEqual(self.student.profile.link3, 'http://www.duckduckgo.com')
        self.student.profile.link3 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link3 = old_link

    def test_student_link_2(self):
        old_link = self.student.profile.link2
        self.assertEqual(self.student.profile.link2, 'http://www.yahoo.com')
        self.student.profile.link2 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link2 = old_link

    def test_student_link_1(self):
        old_link = self.student.profile.link1
        self.assertEqual(self.student.profile.link1, 'http://www.google.com')
        self.student.profile.link1 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link1 = old_link

    def test_student_leadership_roles(self):
        self.assertEqual(self.student.profile.leadership_roles, 'leadership stuff')

    def test_student_skills(self):
        self.assertEqual(self.student.profile.skills, 'lots of super cool skills')

    def test_student_extracurriculars(self):
        self.assertEqual(self.student.profile.extracurriculars, 'some extracurriculars')

    def test_student_volunteer_exp(self):
        self.assertEqual(self.student.profile.volunteering_exp, 'some volunteer experience')

    def test_student_work_exp(self):
        self.assertEqual(self.student.profile.work_exp, 'some work experience')

    def test_student_awards_achievements(self):
        self.assertEqual(self.student.profile.awards_achievements, 'some awards')

    def test_student_teacher_or_counselor_name(self):
        self.assertEqual(self.student.profile.teacher_or_counselor_name, 'teacher teacher')

    def test_student_teacher_or_counselor_email(self):
        old_email = self.student.profile.teacher_or_counselor_email
        self.assertEqual(self.student.profile.teacher_or_counselor_email, 'teacher@gmail.com')
        self.student.profile.teacher_or_counselor_email = 'not an email'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.teacher_or_counselor_email = old_email

    def test_hs_addy(self):
        self.assertEqual(self.student.profile.hs_addy, '123 random st')

    def test_student_hs(self):
        self.assertEqual(self.student.profile.hs, 'humberside')

    def test_student_dob(self):
        prev_dob = self.student.profile.dob
        self.assertEqual(self.student.profile.dob, date.today())
        self.student.profile.dob = 'invalid date'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.dob = prev_dob

    def test_student_first_name(self):
        self.assertEqual(self.student.first_name, 'first')

    def test_student_last_name(self):
        self.assertEqual(self.student.first_name, 'first')

    def test_student_is_student(self):
        self.assertEqual(self.student.is_student, True)

    def test_student_is_employer(self):
        self.assertEqual(self.student.is_employer, False)

    def test_student_profile_picture(self):
        self.assertEqual(self.student.profile_picture.name, 'profile_pictures/default.png')

    def test_expected_student_str(self):
        expected = self.student.email
        self.assertEqual(str(self.student), expected)

    def test_student_profile_attached(self):
        self.assertTrue(self.student.profile)

    def test_student_phone(self):
        old_phone = self.student.profile.phone
        self.assertEqual(self.student.profile.phone, '+12125552368')
        self.student.profile.phone = 'not a phone number'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.phone = old_phone

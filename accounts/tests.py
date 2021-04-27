from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, RequestFactory
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

from mixins.init_accounts import InitAccountsMixin
from .models import *

"""
Tests for the accounts application
"""

class UserTestCase(TestCase, InitAccountsMixin):
    """
    I probably won't get to documenting tests anytime soon tbh.  
    The method names are pretty self explanatory. 
    """

    @classmethod
    def setUpTestData(cls):
        super().set_up()

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

        self.assertRaises(ValidationError, super(UserTestCase, self).student_profile, new_student.id,
                          self.student.profile.phone)

    def test_email(self):
        self.assertRaises(IntegrityError, User.objects.create_user, email=self.student.email, first_name='first',
                          last_name='last',
                          password='password',
                          is_student=True, is_employer=False)
        self.assertEqual(256, User._meta.get_field('email').max_length)

    def test_slug_student(self):
        new_student = User.objects.create_user(email='email@gmail.com', first_name='name first', last_name='name last',
                                               password='password',
                                               is_student=True, is_employer=False)
        super(UserTestCase, self).student_profile(new_student.id, '+12125552369')
        new_student.profile.slug_student()
        self.assertNotEqual(self.student.slug, new_student.slug)
        self.assertEqual(new_student.slug, 'name-first-name-last')
        self.assertEqual(256, User._meta.get_field('slug').max_length)

    def test_slug_employer(self):
        new_employer = User.objects.create_user(email='email@gmail.com', first_name='first', last_name='last',
                                               password='password',
                                               is_student=False, is_employer=True)
        new_employer.employer_profile.company_name = 'company'
        new_employer.save()
        new_employer.employer_profile.slug_employer()
        self.assertNotEqual(self.employer.slug, new_employer.slug)
        self.assertEqual(new_employer.slug, 'company')
        self.assertEqual(256, User._meta.get_field('slug').max_length)

    def test_existing_email(self):
        self.assertRaises(IntegrityError, User.objects.create_user, email='test@gmail.com', first_name='first',
                          last_name='last',
                          password='password',
                          is_student=True, is_employer=False)

    def test_delete_login_redirect(self):
        self.check_login_redirected(reverse('delete'))

    def test_delete_employer_url(self):
        path = reverse('delete')
        user_instance = User.objects.get(email=self.employer_email)
        self.assertTrue(user_instance)

        self.login(user_instance)

        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))
        self.assertRaises(ObjectDoesNotExist, User.objects.get, email=self.employer_email)

    def test_delete_student_url(self):
        user_instance = User.objects.get(email=self.student_email)

        self.login(user_instance)
        self.assertTrue(user_instance)
        response = self.client.get(reverse('delete'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))
        self.assertRaises(ObjectDoesNotExist, User.objects.get, email=self.student_email)

    def test_listings_login_redirect(self):
        self.check_login_redirected(reverse('listings'))

    def test_listings_employer_url(self):
        path = reverse('listings')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_listings_student_url(self):
        self.login(self.student)
        response = self.client.get(reverse('listings'))
        self.assertEqual(response.status_code, 403)

    def test_profile_login_redirect(self):
        self.check_login_redirected(reverse('profile'))

    def test_profile_employer_url(self):
        self.login(self.employer)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].email, self.employer.email)

    def test_profile_student_url(self):
        self.login(self.student)
        response = self.client.get(reverse('profile'))
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
        self.assertEqual(50, EmployerProfile._meta.get_field('company_name').max_length)

    def test_employer_profile_attached(self):
        self.assertTrue(self.employer.employer_profile)

    def test_expected_employer_str(self):
        expected = self.employer.employer_profile.company_name
        self.assertEqual(str(self.employer), expected)

    def test_student_link_4(self):
        old_link = self.student.profile.link4
        self.assertEqual(self.student.profile.link4, None)
        self.student.profile.link4 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link4 = old_link
        self.assertEqual(True, StudentProfile._meta.get_field('link4').null)
        self.assertEqual(True, StudentProfile._meta.get_field('link4').blank)

    def test_student_link_3(self):
        old_link = self.student.profile.link3
        self.assertEqual(self.student.profile.link3, 'http://www.duckduckgo.com')
        self.student.profile.link3 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link3 = old_link
        self.assertEqual(True, StudentProfile._meta.get_field('link3').null)
        self.assertEqual(True, StudentProfile._meta.get_field('link3').blank)

    def test_student_link_2(self):
        old_link = self.student.profile.link2
        self.assertEqual(self.student.profile.link2, 'http://www.yahoo.com')
        self.student.profile.link2 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link2 = old_link
        self.assertEqual(True, StudentProfile._meta.get_field('link2').null)
        self.assertEqual(True, StudentProfile._meta.get_field('link2').blank)

    def test_student_link_1(self):
        old_link = self.student.profile.link1
        self.assertEqual(self.student.profile.link1, 'http://www.google.com')
        self.student.profile.link1 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.link1 = old_link
        self.assertEqual(True, StudentProfile._meta.get_field('link1').null)
        self.assertEqual(True, StudentProfile._meta.get_field('link1').blank)

    def test_student_leadership_roles(self):
        self.assertEqual(self.student.profile.leadership_roles, 'leadership stuff')
        self.assertEqual(True, StudentProfile._meta.get_field('leadership_roles').null)
        self.assertEqual(True, StudentProfile._meta.get_field('leadership_roles').blank)

    def test_student_skills(self):
        self.assertEqual(self.student.profile.skills, 'lots of super cool skills')
        self.assertEqual(True, StudentProfile._meta.get_field('skills').null)
        self.assertEqual(True, StudentProfile._meta.get_field('skills').blank)

    def test_student_extracurriculars(self):
        self.assertEqual(self.student.profile.extracurriculars, 'some extracurriculars')
        self.assertEqual(True, StudentProfile._meta.get_field('extracurriculars').null)
        self.assertEqual(True, StudentProfile._meta.get_field('extracurriculars').blank)

    def test_student_volunteering_exp(self):
        self.assertEqual(self.student.profile.volunteering_exp, 'some volunteer experience')
        self.assertEqual(True, StudentProfile._meta.get_field('volunteering_exp').null)
        self.assertEqual(True, StudentProfile._meta.get_field('volunteering_exp').blank)

    def test_student_work_exp(self):
        self.assertEqual(self.student.profile.work_exp, 'some work experience')
        self.assertEqual(True, StudentProfile._meta.get_field('work_exp').null)
        self.assertEqual(True, StudentProfile._meta.get_field('work_exp').blank)

    def test_student_awards_achievements(self):
        self.assertEqual(self.student.profile.awards_achievements, 'some awards')
        self.assertEqual(True, StudentProfile._meta.get_field('awards_achievements').null)
        self.assertEqual(True, StudentProfile._meta.get_field('awards_achievements').blank)

    def test_student_teacher_or_counselor_name(self):
        self.assertEqual(self.student.profile.teacher_or_counselor_name, 'teacher teacher')
        self.assertEqual(100, StudentProfile._meta.get_field('teacher_or_counselor_name').max_length)
        self.assertEqual(True, StudentProfile._meta.get_field('teacher_or_counselor_name').null)
        self.assertEqual(True, StudentProfile._meta.get_field('teacher_or_counselor_name').blank)

    def test_student_teacher_or_counselor_email(self):
        old_email = self.student.profile.teacher_or_counselor_email
        self.assertEqual(self.student.profile.teacher_or_counselor_email, 'teacher@gmail.com')
        self.student.profile.teacher_or_counselor_email = 'not an email'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.teacher_or_counselor_email = old_email
        self.assertEqual(True, StudentProfile._meta.get_field('teacher_or_counselor_email').null)
        self.assertEqual(True, StudentProfile._meta.get_field('teacher_or_counselor_email').blank)

    def test_student_hs_addy(self):
        self.assertEqual(self.student.profile.hs_addy, '123 random st')
        self.assertEqual(100, StudentProfile._meta.get_field('hs_addy').max_length)
        self.assertEqual(True, StudentProfile._meta.get_field('hs_addy').null)
        self.assertEqual(True, StudentProfile._meta.get_field('hs_addy').blank)

    def test_student_hs(self):
        self.assertEqual(self.student.profile.hs, 'humberside')
        self.assertEqual(100, StudentProfile._meta.get_field('hs').max_length)
        self.assertEqual(True, StudentProfile._meta.get_field('hs').null)
        self.assertEqual(True, StudentProfile._meta.get_field('hs').blank)

    def test_student_dob(self):
        prev_dob = self.student.profile.dob
        self.assertEqual(self.student.profile.dob, date.today())
        self.student.profile.dob = 'invalid date'
        self.assertRaises(ValidationError, self.student.profile.full_clean)
        self.student.profile.dob = prev_dob
        self.assertEqual(True, StudentProfile._meta.get_field('dob').null)
        self.assertEqual(True, StudentProfile._meta.get_field('dob').blank)

    def test_student_str(self):
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
        self.assertEqual(True, StudentProfile._meta.get_field('phone').null)
        self.assertEqual(True, StudentProfile._meta.get_field('phone').blank)

    def test_user_first_name(self):
        self.assertEqual(self.student.first_name, 'first')
        self.assertEqual(self.student.first_name, 'first')

    def test_user_last_name(self):
        self.assertEqual(self.student.first_name, 'first')

    def test_user_is_student(self):
        self.assertEqual(self.student.is_student, True)
        self.assertEqual(self.employer.is_student, False)
        self.assertEqual(False, User._meta.get_field('is_student').default)

    def test_user_is_employer(self):
        self.assertEqual(self.student.is_employer, False)
        self.assertEqual(self.employer.is_employer, True)
        self.assertEqual(False, User._meta.get_field('is_employer').default)

    def test_user_profile_picture(self):
        self.assertEqual(self.student.profile_picture.name, 'profile_pictures/default.png')
        self.assertEqual(self.employer.profile_picture.name, 'profile_pictures/default.png')
        self.assertEqual(True, User._meta.get_field('profile_picture').null)
        self.assertEqual(True, User._meta.get_field('profile_picture').blank)
        self.assertEqual('profile_pictures', User._meta.get_field('profile_picture').upload_to)

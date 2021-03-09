from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import User, StudentProfile, EmployerProfile


class AuthenticationTestCase(TestCase):

    @staticmethod
    def student_registration_data():
        return {
            'email': 'student@gmail.com',
            'first_name': 'student_first',
            'last_name': 'student_last',
            'password1': 'some_password',
            'password2': 'some_password',
            'is_student': True,
            'is_employer': False
        }

    @staticmethod
    def employer_registration_data():
        return {
            'email': 'teacher@gmail.com',
            'first_name': 'teacher_first',
            'last_name': 'teacher_last',
            'password1': 'some_password',
            'password2': 'some_password',
            'is_student': False,
            'is_employer': True,
            'company_name': 'some company'
        }

    def test_not_employer_not_student(self):
        registration_data = self.student_registration_data()
        registration_data['is_student'], registration_data['is_employer'] = False, False

        response = self.client.post(
            reverse('register'), data=registration_data
        )
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_employer_register(self):
        registration_data = self.employer_registration_data()

        response = self.client.post(
            reverse('register'), data=registration_data
        )
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertFalse(response.context)
        user = User.objects.get(email=registration_data['email'])
        self.assertTrue(user)
        self.assertTrue(user.employer_profile in EmployerProfile.objects.all())

    def test_student_register(self):
        registration_data = self.student_registration_data()

        response = self.client.post(
            reverse('register'), data=registration_data
        )
        # print(response.context['form'].errors)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertFalse(response.context)
        user = User.objects.get(email=registration_data['email'])
        self.assertTrue(user)
        self.assertTrue(user.profile in StudentProfile.objects.all())

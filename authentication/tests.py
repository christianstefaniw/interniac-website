from http import HTTPStatus
from defender.test import DefenderTestCaseMixin

from django.test import TestCase
from django.urls import reverse

from accounts.models import User, StudentProfile, EmployerProfile


class AuthenticationTestCase(TestCase, DefenderTestCaseMixin):
    """
    Probably wont get to documenting these, the method names are pretty self explanitory I think
    """

    @staticmethod
    def student_registration_data():
        return {
            'email': 'student@gmail.com',
            'first_name': 'student_first',
            'last_name': 'student_last',
            'password1': 'some_password',
            'password2': 'some_password',
            'student_employer': 'student'
        }

    @staticmethod
    def employer_registration_data():
        return {
            'email': 'teacher@gmail.com',
            'first_name': 'teacher_first',
            'last_name': 'teacher_last',
            'password1': 'some_password',
            'password2': 'some_password',
            'student_employer': 'employer',
            'company_name': 'some company'
        }

    def tearDown(self):
        super().tearDown()

    def register(self, data):
        return self.client.post(
            reverse('register'), data=data
        )

    def all_login_tests(self, data):
        login_data = {'username': data['email'], 'password': data['password2']}
        response = self.client.post(reverse('login'), data=login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('profile'))
        self.client.logout()

        login_data = {'username': data['email'], 'password': 'a_wrong_password'}
        response = self.client.post(reverse('login'), data=login_data, follow=True)
        self.assertTrue(response.context['form'].errors['__all__'])

        login_data = {'username': 'wrongemail@gmail.com', 'password': data['password2']}
        response = self.client.post(reverse('login'), data=login_data, follow=True)
        self.assertTrue(response.context['form'].errors['__all__'])

    def test_employer_login(self):
        data = self.employer_registration_data()
        self.register(data)
        self.all_login_tests(data)

    def test_student_login(self):
        data = self.student_registration_data()
        self.register(data)
        self.all_login_tests(data)

    def test_register_pass_not_match(self):
        registration_data = self.student_registration_data()
        registration_data['password1'], registration_data['password2'] = 'some_rand_password', 'some_rand_password_not_same'

        response = self.register(registration_data)

        self.assertTrue(response.context['form'].errors['password2'])

    def test_register_simple_password(self):
        registration_data = self.student_registration_data()
        registration_data['password1'], registration_data['password2'] = 'simple', 'simple'

        response = self.register(registration_data)

        self.assertTrue(response.context['form'].errors['password2'])

    def test_register_existing_email(self):
        registration_data = self.student_registration_data()

        self.register(registration_data)
        response = self.register(registration_data)
        self.assertTrue(response.context['form'].errors['email'])

    def test_register_student_has_company(self):
        registration_data = self.student_registration_data()
        registration_data['company_name'] = 'a company'

        response = self.register(registration_data)

        self.assertTrue(response.context['form'].errors['student_employer'])

    def test_register_employer_no_company(self):
        registration_data = self.employer_registration_data()
        registration_data['company_name'] = ''

        response = self.register(registration_data)

        self.assertTrue(response.context['form'].errors)

    def test_register_not_employer_not_student(self):
        registration_data = self.student_registration_data()
        registration_data['student_employer'] = ''

        response = self.register(registration_data)

        self.assertTrue(response.context['form'].errors['student_employer'])

    def test_register_employer_register(self):
        registration_data = self.employer_registration_data()

        response = self.register(registration_data)

        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertFalse(response.context)
        user = User.objects.get(email=registration_data['email'])
        self.assertTrue(user)
        self.assertTrue(user.employer_profile in EmployerProfile.objects.all())

    def test_register_student_register(self):
        registration_data = self.student_registration_data()

        response = self.register(registration_data)

        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertFalse(response.context)
        user = User.objects.get(email=registration_data['email'])
        self.assertTrue(user)
        self.assertTrue(user.profile in StudentProfile.objects.all())

    def test_register_invalid_email(self):
        registration_data = self.student_registration_data()
        registration_data['email'] = 'not an email'

        response = self.register(registration_data)

        self.assertTrue(response.context['form'].errors['email'])

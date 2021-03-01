from django.test import TestCase

from .models import *


class UserTestCase(TestCase):
    def setUp(self):
        student = User.objects.create_user(email='test@gmail.com', first_name='first', last_name='last',
                                           password='password',
                                           is_student=True, is_employer=False)
        employer = User.objects.create_user(email='test2@gmail.com', first_name='first', last_name='last',
                                            password='password',
                                            is_student=False, is_employer=True)

        student_profile = StudentProfile.objects.create(user=student)
        student_profile.hs = 'humberside'
        student_profile.phone = 123456789

    def test_user(self):
        student = User.objects.get(email='test2@gmail.com')
        employer = User.objects.get(email='test@gmail.com')

        self.assertEqual(student.first_name, 'first')
        self.assertEqual(student.last_name, 'last')
        self.assertEqual(student.is_student, True)
        self.assertEqual(student.is_employer, False)
        self.assertEqual(student.password, 'password')
        self.assertEqual(student.profile_picture.name, 'profile_pictures/default.png')

        self.assertEqual(employer.first_name, 'first')
        self.assertEqual(employer.last_name, 'last')
        self.assertEqual(employer.is_employer, True)
        self.assertEqual(employer.is_student, False)
        self.assertEqual(employer.password, 'password')
        self.assertEqual(employer.profile_picture.name, 'profile_pictures/default.png')

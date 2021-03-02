from django.test import TestCase
from datetime import date

from .models import *


class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        student = User.objects.create_user(email='test@gmail.com', first_name='first', last_name='last',
                                           password='password',
                                           is_student=True, is_employer=False)
        employer = User.objects.create_user(email='test2@gmail.com', first_name='first', last_name='last',
                                            password='password',
                                            is_student=False, is_employer=True)

        cls.init_student_profile(student.id)
        cls.init_employer_profile(employer.id)

    @staticmethod
    def init_employer_profile(employer_id) -> None:
        employer = User.objects.get(id=employer_id)
        employer_profile = EmployerProfile.objects.create(user=employer)
        employer_profile.company_name = 'some company'

    @staticmethod
    def init_student_profile(student_id) -> None:
        student = User.objects.get(id=student_id)
        student_profile = StudentProfile.objects.create(user=student)
        student_profile.phone = '+10123456789'
        student_profile.dob = date.today()
        student_profile.hs = 'humberside'
        student_profile.hs_addy = '123 random st'
        student_profile.teacher_or_counselor_email = 'teacher@gmail.com'
        student_profile.teacher_or_counselor_name = 'teacher teacher'
        student_profile.awards_achievements = 'some awards'
        student_profile.work_exp = 'some work experience'
        student_profile.volunteering_exp = 'some volunteer experience'
        student_profile.extracurriculars = 'some extra curriculars'
        student_profile.skills = 'lots of super cool skills'
        student_profile.leadership_roles = 'leadership stuff'
        student_profile.link1 = 'http://www.google.com'
        student_profile.link2 = 'http://www.yahoo.com'
        student_profile.link3 = 'http://www.duckduckgo.com'
        student_profile.link4 = None

    def test_student_first_name(self):
        student = User.objects.get(email='test@gmail.com')
        self.assertEqual(student.first_name, 'first')

    def test_student_last_name(self):
        student = User.objects.get(email='test@gmail.com')
        self.assertEqual(student.first_name, 'first')

    def test_student_is_student(self):
        student = User.objects.get(email='test@gmail.com')
        self.assertEqual(student.is_student, True)

    def test_student_is_employer(self):
        student = User.objects.get(email='test@gmail.com')
        self.assertEqual(student.is_employer, False)

    def test_student_profile_picture(self):
        employer = User.objects.get(email='test@gmail.com')
        self.assertEqual(employer.profile_picture.name, 'profile_pictures/default.png')

    def test_expected_student_str(self):
        student = User.objects.get(email='test@gmail.com')
        expected = student.email
        self.assertEqual(str(student), expected)

    def test_student_profile_attached(self):
        student = User.objects.get(email='test@gmail.com')
        self.assertTrue(student.profile)

    def test_employer_first_name(self):
        employer = User.objects.get(email='test2@gmail.com')
        self.assertEqual(employer.first_name, 'first')

    def test_employer_last_name(self):
        employer = User.objects.get(email='test2@gmail.com')
        self.assertEqual(employer.first_name, 'first')

    def test_employer_is_student(self):
        employer = User.objects.get(email='test2@gmail.com')
        self.assertEqual(employer.is_student, False)

    def test_employer_is_employer(self):
        employer = User.objects.get(email='test2@gmail.com')
        self.assertEqual(employer.is_employer, True)

    def test_employer_profile_picture(self):
        employer = User.objects.get(email='test2@gmail.com')
        self.assertEqual(employer.profile_picture.name, 'profile_pictures/default.png')

    def test_expected_employer_str(self):
        employer = User.objects.get(email='test2@gmail.com')
        expected = employer.employer_profile.company_name
        self.assertEqual(str(employer), expected)

    def test_employer_profile_attached(self):
        employer = User.objects.get(email='test2@gmail.com')
        self.assertTrue(employer.employer_profile)

    def test_urls(self):
        pass

from django.core.exceptions import ValidationError
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
        cls.student = User.objects.get(email='test@gmail.com')

    @staticmethod
    def init_employer_profile(employer_id) -> None:
        employer = User.objects.get(id=employer_id)
        employer_profile = EmployerProfile.objects.create(user=employer)
        employer_profile.company_name = 'some company'

    @staticmethod
    def init_student_profile(student_id) -> None:
        student = User.objects.get(id=student_id)
        student_profile = StudentProfile.objects.create(user=student)
        student_profile.phone = '+12125552368'
        student_profile.dob = date.today()
        student_profile.hs = 'humberside'
        student_profile.hs_addy = '123 random st'
        student_profile.teacher_or_counselor_email = 'teacher@gmail.com'
        student_profile.teacher_or_counselor_name = 'teacher teacher'
        student_profile.awards_achievements = 'some awards'
        student_profile.work_exp = 'some work experience'
        student_profile.volunteering_exp = 'some volunteer experience'
        student_profile.extracurriculars = 'some extracurriculars'
        student_profile.skills = 'lots of super cool skills'
        student_profile.leadership_roles = 'leadership stuff'
        student_profile.link1 = 'http://www.google.com'
        student_profile.link2 = 'http://www.yahoo.com'
        student_profile.link3 = 'http://www.duckduckgo.com'
        student_profile.link4 = None
        student_profile.full_clean()
        student_profile.save()

    def test_student_link_4(self):
        self.assertEqual(self.student.profile.link4, None)
        self.student.profile.link4 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)

    def test_student_link_3(self):
        self.assertEqual(self.student.profile.link3, 'http://www.duckduckgo.com')
        self.student.profile.link3 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)

    def test_student_link_2(self):
        self.assertEqual(self.student.profile.link2, 'http://www.yahoo.com')
        self.student.profile.link2 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)

    def test_student_link_1(self):
        self.assertEqual(self.student.profile.link1, 'http://www.google.com')
        self.student.profile.link1 = 'broken link'
        self.assertRaises(ValidationError, self.student.profile.full_clean)

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
        self.assertEqual(self.student.profile.teacher_or_counselor_email, 'teacher@gmail.com')
        self.student.profile.teacher_or_counselor_email = 'not an email'
        self.assertRaises(ValidationError, self.student.profile.full_clean)

    def test_hs_addy(self):
        self.assertEqual(self.student.profile.hs_addy, '123 random st')

    def test_student_hs(self):
        self.assertEqual(self.student.profile.hs, 'humberside')

    def test_student_dob(self):
        self.assertEqual(self.student.profile.dob, date.today())
        self.student.profile.dob = 'invalid date'
        self.assertRaises(ValidationError, self.student.profile.full_clean)

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
        self.assertEqual(self.student.profile.phone, '++12125552368')
        self.student.profile.phone = 'not a phone number'
        self.assertRaises(ValidationError, self.student.profile.full_clean)

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

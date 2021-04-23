from datetime import date

from accounts.models import User


class InitAccountsMixin(object):
    @classmethod
    def set_up(cls):
       
        student = User.objects.create_user(email='test@gmail.com', first_name='first', last_name='last',
                                           password='password',
                                           is_student=True, is_employer=False)
        employer = User.objects.create_user(email='test2@gmail.com', first_name='first', last_name='last',
                                            password='password',
                                            is_student=False, is_employer=True)
                                            
        cls.student_profile(student.id, '+12125552368')
        student = User.objects.get(id=student.id)
        cls.employer_profile(employer.id)
        employer = User.objects.get(id=employer.id)
        cls.student = student
        cls.employer = employer
        cls.password = 'password'
        cls.student_email = 'test@gmail.com'
        cls.employer_email = 'test2@gmail.com'

    @staticmethod
    def employer_profile(employer_id) -> None:
        employer = User.objects.get(id=employer_id)
        employer_profile = employer.employer_profile
        employer_profile.company_name = 'some company'
        employer_profile.company_website = 'http://www.google.com'
        employer_profile.full_clean()
        employer.save()
        employer_profile.save()
        
    @staticmethod
    def student_profile(student_id, phone) -> None:
        student = User.objects.get(id=student_id)
        student_profile = student.profile
        student_profile.phone = phone
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

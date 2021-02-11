from django import forms

from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user']
        labels = {
            'phone': 'Phone Number',
            'dob': 'Date of Birth',
            'hs': 'High School Name',
            'hs_addy': 'High School Address',
            'teacher_or_counselor_email': 'Teacher or Counselor Email',
            'teacher_or_counselor_name': 'Teacher of Counselor Name',
            'awards_achievements': 'Awards and Achievements',
            'work_exp': 'Word Experience',
            'volunteering_experience': 'Volunteering Experience',
            'extracurriculars': 'Extracurricular Activities',
            'skills': 'Skills',
            'leadership_roles': 'Leadership Roles',

        }
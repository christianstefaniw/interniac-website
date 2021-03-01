from django import forms
from django.forms import DateInput, FileInput

from .models import StudentProfile, User


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user']
        widgets = {
            'dob': DateInput(attrs={'type': 'date'})
        }
        labels = {
            'phone': 'Phone Number',
            'dob': 'Date of Birth',
            'hs': 'High School Name',
            'hs_addy': 'High School Address',
            'teacher_or_counselor_email': 'Teacher or Counselor Email',
            'teacher_or_counselor_name': 'Teacher of Counselor Name',
            'awards_achievements': 'Awards and Achievements',
            'work_exp': 'Word Experience',
            'volunteering_exp': 'Volunteering Experience',
            'extracurriculars': 'Extracurricular Activities',
            'skills': 'Skills',
            'leadership_roles': 'Leadership Roles',
        }


class StudentEmailPicture(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'profile_picture': FileInput()
        }
        fields = ['email', 'profile_picture']


class EmailAll(forms.Form):
    subject = forms.CharField(max_length=20)
    body = forms.CharField(widget=forms.Textarea)

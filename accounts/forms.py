from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import StudentProfile, User, EmployerProfile
from helpers.profile_img_validation import validate_profile_img

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'phone': 'Phone Number',
            'dob': 'Date of Birth',
            'hs': 'High School Name',
            'hs_addy': 'High School Address',
            'teacher_or_counselor_email': 'Teacher or Counselor Email',
            'teacher_or_counselor_name': 'Teacher or Counselor Name',
            'awards_achievements': 'Awards and Achievements',
            'work_exp': 'Word Experience',
            'volunteering_exp': 'Volunteering Experience',
            'extracurriculars': 'Extracurricular Activities',
            'skills': 'Skills',
            'leadership_roles': 'Leadership Roles',
        }


class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'profile_picture': forms.FileInput
        }
        fields = ['email', 'profile_picture', 'first_name', 'last_name']

    def clean_profile_picture(self):
        pic = self.cleaned_data['profile_picture']
        if type(pic) is InMemoryUploadedFile:
            return validate_profile_img(pic)
        return pic


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        exclude = ['user']


class EmployerUserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'profile_picture': forms.FileInput
        }
        fields = ['email', 'profile_picture', 'first_name', 'last_name']

    def clean_profile_picture(self):
        pic = self.cleaned_data['profile_picture']
        if type(pic) is InMemoryUploadedFile:
            return validate_profile_img(pic)
        return pic
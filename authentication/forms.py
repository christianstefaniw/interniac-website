from nocaptcha_recaptcha import NoReCaptchaField

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile

from accounts.models import User, EmployerProfile
from helpers.profile_img_validation import validate_profile_img

CHOICES = [('student', 'Student'),
           ('employer', 'Employer')]


class UserCreateForm(UserCreationForm):
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'register-input'}),
                                   help_text='', required=False)
    student_employer = forms.ChoiceField(choices=CHOICES,
                                         widget=forms.RadioSelect,
                                         label='Student or employer')
    captcha = NoReCaptchaField(label='', required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture',
                  'student_employer')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        if self.cleaned_data.get('student_employer') == 'employer':
            user.is_employer = True
            user.is_student = False
        elif self.cleaned_data.get('student_employer') == 'student':
            user.is_student = True
            user.is_employer = False
        user.save()
        if user.is_employer:
            user.employer_profile.company_name = self.cleaned_data.get('company_name')
            user.employer_profile.save()
        return user

    def clean_profile_picture(self):
        pic = self.cleaned_data['profile_picture']
        if type(pic) is InMemoryUploadedFile:
            return validate_profile_img(pic)
        return pic

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if EmployerProfile.objects.filter(company_name=company_name).count() > 0:
            self.add_error('company_name', 'Company already exists')
        return company_name

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        if self.cleaned_data.get('student_employer') == 'employer' and not self.cleaned_data.get('company_name'):
            self.add_error('company_name', 'Enter your companies name')
        if self.cleaned_data.get('student_employer') == 'student' and self.cleaned_data.get('company_name') != '':
            self.add_error('student_employer', 'Student can\'t have a company')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field_name in ('email', 'first_name', 'last_name', 'password1', 'password2',
                           'profile_picture'):

            if field_name == 'is_student':
                self.fields['is_student'].label = 'Student'

            if field_name == 'is_employer':
                self.fields['is_employer'].label = 'Employer'

            self.fields[field_name].help_text = ''

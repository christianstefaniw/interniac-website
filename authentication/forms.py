from django.contrib.auth.forms import UserCreationForm

from accounts.models import StudentProfile, User, EmployerProfile


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture',
                  'is_student', 'is_employer', 'company_name')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=True)
        if user.is_student:
            StudentProfile.objects.create(user=user, )
        elif user.is_employer:
            EmployerProfile.objects.create(user=user, )

        return user

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        print(self.cleaned_data.get('company_name'))
        if not self.cleaned_data.get('is_employer'):
            if not self.cleaned_data.get('is_student'):
                self.add_error('is_student', 'Must be a student or employer')
        if self.cleaned_data.get('is_employer') and not self.cleaned_data.get('company_name'):
            self.add_error('company_name', 'Enter your companies name')
        if self.cleaned_data.get('is_student'):
            if self.cleaned_data.get('company_name') != '':
                self.add_error('is_student', 'Student can\'t have a company')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field_name in ('email', 'first_name', 'last_name', 'password1', 'password2',
                           'profile_picture', 'is_student', 'is_employer', 'company_name'):

            if field_name == 'is_student':
                self.fields['is_student'].label = 'Student'

            if field_name == 'is_employer':
                self.fields['is_employer'].label = 'Employer'

            self.fields[field_name].help_text = ''
            self.fields[field_name].widget.attrs['class'] = 'register-input'

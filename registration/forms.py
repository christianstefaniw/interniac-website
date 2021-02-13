from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import StudentProfile, User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',
                  'is_student', 'is_employer', 'org_website', 'org_name')

    def validate_radio(self):
        if self.data.get('is_employer') == 'on':
            employer = True
        else:
            employer = False

        if self.data.get('is_student') == 'on':
            student = True
        else:
            student = False

        if employer is False and student is False or employer is True and student is True:
            raise ValidationError("Must be a student or employer")

    def clean_is_employer(self):

        self.validate_radio()

        if self.data.get('is_employer') == 'on':
            return True
        else:
            return False

    def clean_is_student(self):
        if self.data.get('is_student') == 'on':
            return True
        else:
            return False

    def save(self, commit=True):
        data = {'email': self.data.get('email'), 'first_name': self.data.get('first_name'),
                'last_name': self.data.get('last_name'), 'password': self.data.get('password1'),
                'is_student': self.cleaned_data['is_student'],
                'is_employer': self.cleaned_data['is_employer']}

        if self.cleaned_data['is_student']:
            user = User.objects.create_user(**data)
        else:
            user = User.objects.create_user(**data,
                                            org_name=self.data.get('org_name'),
                                            org_website=self.data.get('org_website'),
                                            )

        StudentProfile.objects.create(
            user=user,
        )

        return user

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field_name in ("email", 'first_name', 'last_name', "password1", "password2", 'is_student', 'is_employer',
                           'org_website', 'org_name'):

            if field_name == "is_student":
                self.fields["is_student"].label = "Student"

            if field_name == "is_employer":
                self.fields["is_employer"].label = "Employer"

            if field_name == "org_name":
                self.fields["org_name"].label = "Organization Name"
            if field_name == "org_website":
                self.fields["org_website"].label = "Organization Website"

            self.fields[field_name].help_text = ''
            self.fields[field_name].widget.attrs['class'] = 'register-input'

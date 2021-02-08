from django.contrib.auth.forms import UserCreationForm

from accounts.models import StudentProfile, User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", 'first_name', 'last_name', "password1", "password2", 'is_student', 'is_staff')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit)

        user.is_client = True

        StudentProfile.objects.create(
            user=user,
        )

        return user

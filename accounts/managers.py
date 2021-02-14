from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, is_student,
                    is_employer, profile_picture=None):

        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))

        user.first_name = first_name
        user.last_name = last_name

        user.set_password(password)  # change password to hash

        user.profile_picture = profile_picture

        user.is_student = is_student
        user.is_employer = is_employer

        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_employer=False,
            is_student=False
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

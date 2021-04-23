from django.contrib.auth.models import BaseUserManager

'''
Custom user manager
Provides helper methods for user management
'''
class UserManager(BaseUserManager):
    '''
    Helper method for creating a generic user

    @param is_student: if the user is a student
    @param is_employer: if the user is an emoloyer
    @return: a ```User``` object
    '''
    def create_user(self, email, first_name, last_name, password, is_student,
                    is_employer, profile_picture=None):

        user = self.model(email=self.normalize_email(email))

        user.first_name = first_name
        user.last_name = last_name

        user.set_password(password)  # change password to hash

        if profile_picture:
            user.profile_picture = profile_picture

        user.is_student = is_student
        user.is_employer = is_employer

        user.save()
        return user

    '''
    Helper method for creating a superuser user

    @return: a ```User``` object
    '''
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

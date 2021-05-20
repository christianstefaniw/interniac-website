from django.contrib.auth import login
from django.forms import model_to_dict

from accounts.forms import EmployerProfileForm, StudentProfileForm, UserForm
from accounts.models import EmployerProfile, User, StudentProfile

"""
Helper classes for the accounts application  
Currently we support the following 2 helper classes:

1. **`Employer`** - retreiving and saving employer account
2. **`Student`** - retreiving and saving student account

"""


class Employer(object):
    """
    This class provides helper methods for viewing and mutating an employer account
    """

    def __init__(self, request):
        """
        @type request: `request`  
        @param request: the user's current request object
        """

        self.request = request

    def employer_profile(self) -> EmployerProfileForm:
        """
        Create employer profile form with initial data of the current users profile data in
        order to autofill user's account data in their profile page

        @rtype: `EmployerProfileForm`  
        @returns: `EmployerProfileForm` with current user's profile data filled in
        """

        initial_data = model_to_dict(self.request.user.employer_profile)
        profile = EmployerProfileForm(
            initial=initial_data)
        return profile

    def employer_user(self) -> UserForm:
        """
        Create general user form with initial data of the current users data

        @rtype: `UserForm`  
        @returns: `UserForm` with current user's data filled in
        """

        initial_data = model_to_dict(self.request.user)
        user_form = UserForm(
            initial=initial_data)
        return user_form

    @staticmethod
    def save_both(request):
        """
        Edit, validate and save both the general user form and the employer profile form

        @type request: `request`  
        @param request: the user's current request object  
        @rtype: `UserForm`, `ProfileForm`  
        @returns: validated `UserForm` and `ProfileForm` upon failed validation 
        or `None` upon successful validation
        """

        profile = EmployerProfile.objects.get(user=request.user)
        profile_form = EmployerProfileForm(request.POST, instance=profile)
        user = User.objects.get(email=request.user.email)
        user_form = UserForm(
            request.POST, request.FILES, instance=user)
        if all((profile_form.is_valid(), user_form.is_valid())):
            # if the user changed their email, login again
            if user.email != request.user:
                login(request, user)
            user_form.save()
            profile_form.save()
            return None, None
        else:
            return profile_form, user_form


class Student(object):
    """
    This class provides helper methods for viewing and mutating a student account
    """

    def __init__(self, request):
        """
        @type request: `request`  
        @param request: the user's current request object
        """

        self.request = request

    def student_profile(self) -> StudentProfileForm:
        """
        Create student profile form with initial data of the current users profile data in
        order to autofill user's account data in their profile page.

        @rtype: `StudentProfileForm`  
        @returns: `StudentProfileForm` with current user's profile data filled in
        """

        current_data = StudentProfile.objects.get(user=self.request.user)
        profile = StudentProfileForm(initial=model_to_dict(current_data))
        return profile

    def student_user(self):
        """
        Create general user form with initial data of the current users data

        @rtype: `UserForm`  
        @returns: `UserForm` with current user's data filled in
        """

        email_picture = UserForm(
            initial=model_to_dict(self.request.user))
        return email_picture

    @staticmethod
    def save_both(request):
        """
        Edit, validate and save both the general user form and the employer profile form

        @type request: `request`  
        @param request: the user's current request object  
        @rtype:  `UserForm`, `ProfileForm`  
        @returns: validated `UserForm` and `ProfileForm` upon failed validation
        or `None` upon successful validation
        """

        profile = StudentProfile.objects.get(user=request.user)
        profile_form = StudentProfileForm(request.POST, instance=profile)
        user = User.objects.get(email=request.user.email)
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if all((profile_form.is_valid(), user_form.is_valid())):
            # if the user changed their email, login again
            if user.email != request.user:
                login(request, user)
            user_form.save()
            profile_form.save()
            return None, None
        else:
            return profile_form, user_form

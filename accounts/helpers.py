from PIL import Image

from django.contrib.auth import login
from django.forms import model_to_dict
from django.shortcuts import redirect
from django import forms

from accounts.forms import EmployerProfileForm, StudentProfileForm, UserForm
from accounts.models import EmployerProfile, User, StudentProfile


'''
This class provides helper functions for viewing and mutating an employer account

@param request: the user's current request object
'''


class Employer(object):
    def __init__(self, request):
        self.request = request

    '''
    Create employer profile form with initial data of the current users profile data in
    order to autofill user's account data in their profile page

    @returns: ```EmployerProfileForm``` with current user's profile data filled in
    '''

    def employer_profile(self) -> EmployerProfileForm:
        initial_data = model_to_dict(self.request.user.employer_profile)
        profile = EmployerProfileForm(
            initial=initial_data)
        return profile

    '''
    Create general user form with initial data of the current users data

    @returns: ```UserForm``` with current user's data filled in
    '''

    def employer_user(self) -> UserForm:
        initial_data = model_to_dict(self.request.user)
        user_form = UserForm(
            initial=initial_data)
        return user_form

    '''
    Edit, validate and save both the general user form and the employer profile form

    @param request: the user's current request object
    @returns: validated ```UserForm``` and ```ProfileForm``` upon failed validation
     or ```None``` upon successful validation
    '''
    @staticmethod
    def save_both(request):
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


'''
This class provides helper functions for viewing and mutating a student account

@param request: the user's current request object
'''


class Student(object):
    def __init__(self, request):
        self.request = request

    '''
    Create student profile form with initial data of the current users profile data in
    order to autofill user's account data in their profile page

    @returns: ```StudentProfileForm``` with current user's profile data filled in
    '''

    def student_profile(self) -> StudentProfileForm:
        current_data = StudentProfile.objects.get(user=self.request.user)
        profile = StudentProfileForm(initial=model_to_dict(current_data))
        return profile

    '''
    Create general user form with initial data of the current users data

    @returns: ```UserForm``` with current user's data filled in
    '''

    def student_user(self):
        email_picture = UserForm(
            initial=model_to_dict(self.request.user))
        return email_picture

    '''
    Edit, validate and save both the general user form and the employer profile form

    @param request: the user's current request object
    @returns: validated ```UserForm``` and ```ProfileForm``` upon failed validation
     or ```None``` upon successful validation
    '''
    @staticmethod
    def save_both(request):
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

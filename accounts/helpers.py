import os

from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.forms import model_to_dict
from django.shortcuts import redirect

from accounts.forms import *
from accounts.models import EmployerProfile, User, StudentProfile
from home.models import EmailSignup


def email_all(request):
    form = EmailAll(request.POST)

    if form.is_valid():
        receiver_list = [email for email in EmailSignup.objects.all()]

        EmailMessage(body=form.cleaned_data.get('body'), from_email=os.environ.get('EMAIL'),
                     to=receiver_list, subject=form.cleaned_data.get('subject'),
                     ).send()
        return redirect('success')
    else:
        return redirect('error')


class _Employer:

    def __init__(self, request):
        self.request = request

    def employer_profile(self):
        current_data = EmployerProfile.objects.get(user=self.request.user)
        profile = EmployerProfileForm(initial=model_to_dict(current_data))
        return profile

    def employer_user(self):
        email_picture_name = EmployerUserForm(initial=model_to_dict(self.request.user))
        return email_picture_name

    @staticmethod
    def save_both(request):
        profile = EmployerProfile.objects.get(user=request.user)
        profile_form = EmployerProfileForm(request.POST, instance=profile)
        user = User.objects.get(email=request.user.email)
        user_form = EmployerUserForm(request.POST, request.FILES, instance=user)
        if all((profile_form.is_valid(), user_form.is_valid())):
            if user.email != request.user:
                login(request, user)
            user_form.save()
            profile.save()


class _Student:

    def __init__(self, request):
        self.request = request

    def student_profile(self):
        current_data = StudentProfile.objects.get(user=self.request.user)
        profile = StudentProfileForm(initial=model_to_dict(current_data))
        return profile

    def student_user(self):
        email_picture = StudentUserForm(initial=model_to_dict(self.request.user))
        return email_picture

    @staticmethod
    def save_both(request):
        profile = StudentProfile.objects.get(user=request.user)
        profile_form = StudentProfileForm(request.POST, instance=profile)
        user = User.objects.get(email=request.user.email)
        user_form = StudentUserForm(request.POST, request.FILES, instance=user)
        if all((profile_form.is_valid(), user_form.is_valid())):
            if user.email != request.user:
                login(request, user)
            user_form.save()
            profile.save()

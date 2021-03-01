import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.forms.models import model_to_dict

from home.models import EmailSignup
from marketplace.models import Listing
from .forms import StudentProfileForm, StudentEmailPicture, EmailAll
from .models import StudentProfile, User, EmployerProfile


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def post(self, request, **kwargs):
        if 'subject' in request.POST and 'body' in request.POST:
            return email_all(request)
        else:
            _Student.save_both(request)
        return super(Profile, self).render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_student:
            student = _Student(self.request)
            context['student_profile_form'] = student.student_profile()
            context['student_email_picture_form'] = student.student_email_picture_form()

        if self.request.user.is_employer:
            employer = _Employer(self.request.user)
            context['marketplace_listings'] = employer.marketplace_listings()

        if self.request.user.is_staff or self.request.user.is_superuser:
            context['form'] = EmailAll()

        return context


class Listings(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/employer/listings.html'


def email_all(request):
    form = EmailAll(request.POST)

    if form.is_valid():
        receiver_list = [email for email in EmailSignup.objects.all()]

        EmailMessage(body=form.cleaned_data.get('body'), from_email=os.environ.get('EMAIL'),
                     to=receiver_list, subject=form.cleaned_data.get('subject'),
                     ).send()
        return redirect(reverse('success'))
    else:
        return redirect(reverse('error'))


@login_required
def delete_user(request):
    user = User.objects.get(email=request.user)

    if user.is_superuser:
        user.delete()
        return redirect(reverse('login'))

    if user.is_employer:
        user_profile = EmployerProfile.objects.get(user=user)
    else:
        user_profile = StudentProfile.objects.get(user=user)
    user_profile.delete()
    user.delete()
    return redirect(reverse('login'))


class _Employer:

    def __init__(self, user):
        self.user = user

    def marketplace_listings(self):
        return Listing.objects.filter(company=self.user)


class _Student:

    def __init__(self, request):
        self.request = request

    def student_profile(self):
        current_data = StudentProfile.objects.get(user=self.request.user)
        profile = StudentProfileForm(initial=model_to_dict(current_data))
        return profile

    def student_email_picture_form(self):
        email_picture = StudentEmailPicture(initial=model_to_dict(self.request.user))
        return email_picture

    @staticmethod
    def save_both(request):
        profile = StudentProfile.objects.get(user=request.user)
        profile_form = StudentProfileForm(request.POST, instance=profile)
        user = User.objects.get(email=request.user)
        email_picture_form = StudentEmailPicture(request.POST, request.FILES, instance=user)
        if all((profile_form.is_valid(), email_picture_form.is_valid())):
            if user.email != request.user:
                login(request, user)
            email_picture_form.save()
            profile.save()

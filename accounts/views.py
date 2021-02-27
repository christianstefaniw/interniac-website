from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.forms.models import model_to_dict

from marketplace.models import Listing
from .forms import StudentProfileForm, StudentEmailPicture
from .models import StudentProfile, User, EmployerProfile


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def post(self, request, **kwargs):
        return super(Profile, self).render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_student:
            student = _Student(self.request)
            if self.request.method == 'POST':
                student.save_both()
            context['student_profile_form'] = student.student_profile()
            context['student_email_picture_form'] = student.student_email_picture_form()
        if self.request.user.is_employer:
            employer = _Employer(self.request.user)
            context['marketplace_listings'] = employer.marketplace_listings()
        return context


def delete_user(request, id):
    user = User.objects.get(id=id)

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
        current_data = User.objects.get(email=self.request.user)
        email_picture = StudentEmailPicture(initial=model_to_dict(current_data))
        return email_picture

    def save_both(self):
        profile = StudentProfile.objects.get(user=self.request.user)
        profile_form = StudentProfileForm(self.request.POST, instance=profile)
        user = User.objects.get(email=self.request.user)
        email_picture_form = StudentEmailPicture(self.request.POST, self.request.FILES, instance=user)
        if all((profile_form.is_valid(), email_picture_form.is_valid())):
            if user.email != self.request.user:
                login(self.request, user)
            email_picture_form.save()
            profile.save()



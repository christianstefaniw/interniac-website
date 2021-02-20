from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from marketplace.models import Listing
from .forms import StudentProfileForm
from .models import StudentProfile, User, EmployerProfile


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_student:
            student = _Student()
            context['student_profile_form'] = student.student_profile(self.request)
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
        return Listing.objects.filter(org=self.user)


class _Student:

    def student_profile(self, request):
        student_form = self.create_student_form(request)
        if request.method == 'POST':
            if student_form.is_valid():
                student_form.save()

        return student_form

    @staticmethod
    def create_student_form(request):
        if request.method == 'POST':
            instance = StudentProfile.objects.get(user=request.user)
            form = StudentProfileForm(request.POST, instance=instance)
        else:
            current_data = StudentProfile.objects.get(user=request.user)
            form = StudentProfileForm(initial=current_data.__dict__)
        return form

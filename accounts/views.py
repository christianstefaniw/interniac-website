from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from marketplace.models import Listing
from .forms import StudentProfileForm
from .models import StudentProfile, User


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_student:
            context['student_profile_form'] = Student.student_profile(self.request)
        if self.request.user.is_employer:
            employer = Employer(self.request.user)
            context['marketplace_listings'] = employer.marketplace_listings()
        return context


def unapply(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.applications.remove(request.user)
    return redirect('success')


class Employer:

    def __init__(self, user):
        self.user = user

    def marketplace_listings(self):
        return Listing.objects.filter(org=self.user)


class Student:

    @staticmethod
    def student_profile(request):
        student_form = Student.create_student_form(request)
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

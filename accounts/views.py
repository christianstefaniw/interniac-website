from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import EmailAll
from .helpers import email_all, _Student, _Employer
from .models import StudentProfile, User, EmployerProfile


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy('login')

    def post(self, request, **kwargs):
        if 'subject' in request.POST and 'body' in request.POST:
            return email_all(request)
        elif 'hs' in request.POST:
            _Student.save_both(request)
        elif 'company_website' in request.POST:
            _Employer.save_both(request)
        return super(Profile, self).render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_student:
            student = _Student(self.request)
            context['student_profile_form'] = student.student_profile()
            context['student_user_form'] = student.student_user()

        if self.request.user.is_employer:
            employer = _Employer(self.request)
            context['employer_profile_form'] = employer.employer_profile()
            context['employer_user_form'] = employer.employer_user()

        if self.request.user.is_staff or self.request.user.is_superuser:
            context['form'] = EmailAll()

        return context


class Listings(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/employer/listings.html'


@login_required
def delete_user(request):
    user = User.objects.get(email=request.user)

    if user.is_superuser:
        user.delete()
        return redirect('login')

    if user.is_employer:
        user_profile = EmployerProfile.objects.get(user=user)
    else:
        user_profile = StudentProfile.objects.get(user=user)
    user_profile.delete()
    user.delete()
    return redirect('login')


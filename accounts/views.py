from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from careers.forms import CareerForm
from .forms import EmailAll
from .helpers import email_all, Student, Employer, save_career
from .models import StudentProfile, User, EmployerProfile


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy('login')

    def post(self, request, **kwargs):
        if 'subject' in request.POST and 'body' in request.POST:
            return email_all(request)

        elif 'hs' in request.POST:
            profile_form, user_form = Student.save_both(request)
            if profile_form or user_form:
                return super(Profile, self).render_to_response(self.get_context_data(profile_form=profile_form,
                                                                                     user_form=user_form))

        elif 'company_website' in request.POST:
            profile_form, user_form = Employer.save_both(request)
            if profile_form or user_form:
                return super(Profile, self).render_to_response(self.get_context_data(profile_form=profile_form,
                                                                                     user_form=user_form))

        elif 'content' in request.POST and (self.request.user.is_staff or self.request.user.is_superuser):
            return save_career(request)

        return super(Profile, self).render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        if self.request.user.is_student:
            student = Student(self.request)
            if kwargs.get('profile_form') and kwargs.get('user_form'):
                context['student_profile_form'] = kwargs.get('profile_form')
                context['student_user_form'] = kwargs.get('user_form')
            else:
                context['student_profile_form'] = student.student_profile()
                context['student_user_form'] = student.student_user()

        if self.request.user.is_employer:
            employer = Employer(self.request)
            if kwargs.get('profile_form') and kwargs.get('user_form'):
                context['employer_profile_form'] = kwargs.get('profile_form')
                context['employer_user_form'] = kwargs.get('user_form')
            else:
                context['employer_profile_form'] = employer.employer_profile()
                context['employer_user_form'] = employer.employer_user()

        if self.request.user.is_staff or self.request.user.is_superuser:
            context['form'] = EmailAll()
            context['new_career'] = CareerForm()

        return context


class Listings(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/employer/listings.html'


@login_required
def delete_user(request):
    user = User.objects.get(email=request.user.email)

    if user.is_superuser:
        user.delete()
        return redirect('login')

    user.delete()
    return redirect('login')

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied

from .helpers import Student, Employer
from mixins.employer_required import EmployerRequiredMixin

class Profile(LoginRequiredMixin, TemplateView):
    '''
    Renders a ``UserForm``` and either a ```StudentProfileForm``` or a ```EmployerProfileForm``` depending on the request
    '''

    template_name = 'accounts/profile.html'

    def post(self, request, **kwargs):
        '''
        Overrides the default ```TemplateView``` ```post``` method. Validates and attempts to save a 
        ```UserForm``` and either a ```StudentProfileForm``` or a ```EmployerProfileForm``` depending on the request

        @param request: a request object
        @returns: ```TemplateResponse``` object with the current context
        '''

        if 'hs' in request.POST:
            # only a student account can have the ```hs``` field, so this condition has to be for student account
            profile_form, user_form = Student.save_both(request)
            if profile_form or user_form:
                return super(Profile, self).render_to_response(self.get_context_data(profile_form=profile_form,
                                                                                     user_form=user_form))

        elif 'company_website' in request.POST:
            # only a employer account can have the ```company_website``` field, so this condition has to be for employer account
            profile_form, user_form = Employer.save_both(request)
            if profile_form or user_form:
                return super(Profile, self).render_to_response(self.get_context_data(profile_form=profile_form,
                                                                                     user_form=user_form))

        return super(Profile, self).render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        '''
        Overrides the default ```TemplateView``` ```get_context_data``` method to provide
        additional information (context) to the template
        '''

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

        return context


class Listings(EmployerRequiredMixin, TemplateView):
    '''Renders all of an employers listings'''

    template_name = 'accounts/employer/listings.html'

    def get(self, request, *args, **kwargs):
        return super(Listings, self).get(request, args, kwargs)


@login_required
def delete_user(request):
    '''
    Deletes the current user

    @param request: the current request object
    '''
    request.user.delete()
    return redirect('login')

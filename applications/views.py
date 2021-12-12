from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, RedirectView
from django.core.exceptions import PermissionDenied

from accounts.models import User
from decorators.student_required import student_required
from decorators.employer_required import employer_required
from marketplace.models import Listing
from mixins.employer_required import EmployerRequiredMixin
from mixins.student_required import StudentRequiredMixin
from .helpers import *


@login_required
@student_required
def apply_and_email(request, listing_id):
    """
    This function based view applies the current user to the selected internship and emails the
    listing owner that the user applied  

    @param listing_id: the id of the listing that the user wants to apply for  
    @type listing_id: `int`  
    """
    listing = Listing.objects.get(id=listing_id)

    if not listing.has_student_already_applied(request.user):
        Applied.applied_email(request.user, listing)

    listing.apply(request.user)
    redirect_where = request.GET.get('redirect')
    if redirect_where == 'profile':
        return redirect(request.user)
    elif redirect_where == 'success':
        return render(request, 'success-error/success-applied.html',
                      context={'which': listing})
    else:
        return HttpResponse(f'<button class="apply-unapply-btn" onclick="unapply({listing_id}, this)">Unapply</button>')


@login_required
@student_required
def unapply(request, listing_id):
    """
    This function based view unapplies the current user from the selected listing  

    @param listing_id: the id of the listing that the user wants to unapply to  
    @type param: `int`  
    """
    listing = Listing.objects.get(id=listing_id)
    listing.unapply(request.user)
    redirect_where = request.GET.get('redirect')
    if redirect_where == 'profile':
        return redirect('applications')
    elif redirect_where == 'success':
        return render(request, 'success-error/success-unapplied.html',
                      context={'which': listing})
    else:
        return HttpResponse(f'<button class="apply-unapply-btn" onclick="apply({listing_id}, this)">Apply</button>')


@login_required
def accept_and_email(request, listing_id, student_id):
    """
    This function based view accepts an application and emails the applicant that they were accepted  

    @param listing_id: the id of the listing that the applicant applied to  
    @type listing_id: `int`  
    @param student_id: the id of the user that is being accepted  
    @type student_id: `int`  
    """
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionDenied

    student = User.objects.get(id=student_id)
    listing.accept(student)
    AcceptStudent.accept_student_email(student, listing)
    return render(request, 'success-error/success-accepted-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required
def reject_and_email(request, listing_id, student_id):
    """
    This function based view rejects an application and emails the applicant that they were rejected  

    @param listing_id: the id of the listing that the applicant applied to  
    @type listing_id: `int`  
    @param student_id: the id of the user that is being accepted  
    @type student_id: `int`  
    """
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionDenied

    student = User.objects.get(id=student_id)
    listing.reject(student)
    RejectStudent.reject_student_email(student, listing)
    return render(request, 'success-error/success-rejected-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required
def request_interview_and_email(request, listing_id, student_id):
    """
    This function based view requests an interview from an applicant and 
    sends the applicant an email that an interview was requested  

    @param listing_id: the id of the listing that the applicant applied to  
    @type listing_id: `int`  
    @param student_id: the id of the user that is being requested  
    @type student_id: `int`  
    """
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionDenied

    student = User.objects.get(id=student_id)
    listing.request_interview(student)
    RequestInterview.request_interview_email(student, listing)
    return render(request, 'success-error/success-requested-interview.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


class SingleApplication(LoginRequiredMixin, TemplateView):
    """
    This class based view allows the listing owner to view an applicants application  

    @kwarg listing_slug: slug id for the selected listing  
    @type listing_slug: `slug`  
    @kwarg user_slug: the slug id for the applicants account  
    @type user_slug: `slug`  
    """

    template_name = 'applications/employer/single-application.html'

    def get(self, *args, **kwargs):
        """
        This method overrides the `TemplateView` get method. It validates that the current user is the owner of the requested listing  
        """
        if self.request.user != self.get_listing().company:
            raise PermissionDenied
        return super(SingleApplication, self).get(self.request)

    def get_context_data(self, **kwargs):
        """
        This method overrides the default `TemplateView` `get_context_data` method to provide
        additional information (context) to the template  
        """
        context = super().get_context_data()
        context['student'] = self.get_student()
        context['listing'] = self.get_listing()
        return context

    def get_student(self):
        """
        This method retrieves the applicants account  

        @returns `User` object  
        """
        return User.objects.get(slug=self.kwargs['user_slug'])

    def get_listing(self):
        """
        This method retrieves the listing that the applicant applied to   

        @returns `Listing` object  
        """
        return Listing.objects.get(slug=self.kwargs['listing_slug'])


class AllApplications(EmployerRequiredMixin, TemplateView):
    """
    This class based view render all applications for a certian listing  
    """
    template_name = 'applications/employer/all/all-applications.html'

    def get_context_data(self, **kwargs):
        """
        This method overrides the default `TemplateView` `get_context_data` method to provide 
        additional information (context) to the template  

        @kwarg slug: the slug identifer for a listing  
        @type slug: `slug`   
        """

        context = super(AllApplications, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllAcceptances(EmployerRequiredMixin, TemplateView):
    """
    This class based view renders all of the acceptances for a selected listing  

    @kwarg slug: the slug identifer for a listing  
    @type slug: `slug`  
    """

    template_name = 'applications/employer/all/all-acceptances.html'

    def get_context_data(self, **kwargs):
        """
        This method overrides the default `TemplateView` `get_context_data` method to provide additional 
        information (context) to the template  
        """
        context = super(AllAcceptances, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllRejections(EmployerRequiredMixin, TemplateView):
    """
    This class based view renders all of the rejections for a selected listing  

    @kwarg slug: the slug identifer for a listing  
    @type slug: `slug`  
    """

    template_name = 'applications/employer/all/all-rejections.html'

    def get_context_data(self, **kwargs):
        """
        This method overrides the default `TemplateView` `get_context_data` method to provide additional 
        information (context) to the template  
        """
        context = super(AllRejections, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllInterviewRequests(EmployerRequiredMixin, TemplateView):
    """
    This class based view renders all of the interview requests for a selected listing  

    @kwarg slug: the slug identifer for a listing  
    @type slug: `slug`  
    """

    template_name = 'applications/employer/all/all-interviewrequests.html'

    def get_context_data(self, **kwargs):
        """
        This method overrides the default `TemplateView` `get_context_data` method to provide additional 
        information (context) to the template  
        """
        context = super(AllInterviewRequests, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllAwaitingConfirm(EmployerRequiredMixin, TemplateView):
    """
    This class based view renders all of the acceptances awaiting confirmation from the applicant  

    @kwarg slug: the slug identifer for a listing  
    @type slug: `slug`  
    """

    template_name = 'applications/employer/all/all-awaiting-confirm.html'

    def get_context_data(self, **kwargs):
        """
        This method overrides the default `TemplateView` `get_context_data` method to provide additional 
        information (context) to the template  
        """
        context = super(AllAwaitingConfirm, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class Acceptances(LoginRequiredMixin, TemplateView):
    """
    This class based view renders the acceptances template. May not render all acceptances.  
    """

    template_name = 'applications/acceptances.html'


class Rejections(LoginRequiredMixin, TemplateView):
    """
    This class based view renders the rejections template. May not render all rejections.  
    """

    template_name = 'applications/rejections.html'


class InterviewRequests(LoginRequiredMixin, TemplateView):
    """
    This class based view renders the interview requests template. May not render all interview requests.  
    """

    template_name = 'applications/interview-requests.html'


class AwaitingConfirm(TemplateView):
    """
    This class based view renders the awaiting confirmation template. May not render all applications awaiting confrimation.  
    """

    template_name = 'applications/awaiting-confirm.html'


class ArchiveAcceptance(LoginRequiredMixin, RedirectView):
    """
    This class based view archives an acceptance and redirects to the `acceptances` url  

    @kwarg listing_id: the id of the listing that the user was accepted for  
    @type listing_id: `int`  
    @kwarg student_id: the id of the student that was accepted  
    @type student_id: `int`
    """

    url = reverse_lazy('acceptances')

    def get_redirect_url(self, *args, **kwargs):
        """
        This method overrides the `RedirectView` `get_redirect_url` method.  
        This method also archives an acceptance with slightly different functionality depending on if the current user if an employer or student.  
        """
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))

        if listing.company != self.request.user and self.request.user != user:
            raise PermissionDenied

        if self.request.user.is_employer:
            # archive the acceptance for the user passed to this view
            self.request.user.employer_profile.archive_acceptance(
                listing, user)
        elif self.request.user.is_student:
            # archive the acceptance for the active user
            user.profile.archive_acceptance(listing)

        return super().get_redirect_url(*args, **kwargs)


class ArchiveInterviewRequest(LoginRequiredMixin, RedirectView):
    """
    This class based view archives an interview request and redirects to the `interview_requests` url  

    @kwarg listing_id: the id of the listing that the user was requested for  
    @type listing_id: `int`  
    @kwarg student_id: the id of the student that was requested  
    """

    url = reverse_lazy('interview_requests')

    def get_redirect_url(self, *args, **kwargs):
        """
        This method overrides the `RedirectView` `get_redirect_url` method. 
        This method also archives an intervew request with slightly different functionality depending on if the current user if an employer or student.  
        """
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionDenied
        if self.request.user.is_employer:
            # archive the interview request for the user passed to this view
            self.request.user.employer_profile.archive_interview_request(
                listing, user)
        elif self.request.user.is_student:
            # archive the interview request for the active user
            user.profile.archive_interview_request(listing)
        return super().get_redirect_url(*args, **kwargs)


class ArchiveRejection(LoginRequiredMixin, RedirectView):
    """
    This class based view archives a rejection and redirects to the `interview_requests` url  

    @kwarg listing_id: the id of the listing that the user was rejected for  
    @type listing_id: `int`  
    @kwarg student_id: the id of the student that was rejected  
    """

    url = reverse_lazy('rejections')

    def get_redirect_url(self, *args, **kwargs):
        """
        This method overrides the `RedirectView` `get_redirect_url` method.  
        This method also archives a rejection with slightly different functionality depending on if the current user if an employer or student  
        """
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionDenied
        if self.request.user.is_employer:
            # archive the interview request for the user passed to this view
            self.request.user.employer_profile.archive_rejection(listing, user)
        elif self.request.user.is_student:
            # archive the interview request for the active user
            user.profile.archive_rejection(listing)
        return super().get_redirect_url(*args, **kwargs)


class DeclineAcceptanceAndEmail(RedirectView, StudentRequiredMixin):
    """
    When a student is accepted, they have the opprotunity to confirm/decline their acceptance.  
    This class based view declines an acceptance and emails the user that accepted them that they declined  

    @kwarg listing_id: the id of the listing that the student was accepted to  
    @type listing_id: `int`  
    """

    url = reverse_lazy('awaiting_confirm')

    def get_redirect_url(self, *args, **kwargs):
        """
        This method overrides the `RedirectView` `get_redirect_url` method.  
        This method also declines the acceptance and emails the employer  
        """
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        if not listing.check_if_accepted(self.request.user):
            raise PermissionDenied
        listing.decline_acceptance(self.request.user)
        DeclineAcceptance.declined_acceptance_email(self.request.user, listing)
        return super().get_redirect_url(*args, **kwargs)


class ConfirmAcceptanceAndEmail(RedirectView, StudentRequiredMixin):
    """
    When a student is accepted, they have the opprotunity to confirm/decline their acceptance.  
    This class based view confirms an acceptance and emails the user that accepted them that they confirmed  

    @kwarg listing_id: the id of the listing that the student was accepted to  
    @type listing_id: `int`  
    """

    url = reverse_lazy('awaiting_confirm')

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        if not listing.check_if_accepted(self.request.user):
            raise PermissionDenied
        listing.confirm_acceptance(self.request.user)
        ConfirmAcceptance.confirmed_acceptance_email(
            self.request.user, listing)
        return super().get_redirect_url(*args, **kwargs)


class Applications(LoginRequiredMixin, TemplateView):
    """
    This class based view renders the applications template.  
    """

    template_name = 'applications/applications.html'


@login_required
@employer_required
def clear_application_notifications(request, slug):
    """
    This function based view clears all of an employers application
    notifications for a certian listing and redirects to the `applications` url.  

    @param slug: the slug identifier for the selected listing  
    @type slug: `slug`  
    """
    listing = Listing.objects.get(slug=slug)
    notifs = request.user.notifications.unread()
    notifs = notifs.filter(actor_object_id=listing.id)
    notifs.mark_all_as_deleted()
    return redirect(reverse('applications'))

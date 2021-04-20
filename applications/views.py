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

__all__ = ['AllApplications', 'AllAcceptances', 'AllRejections', 'AllInterviewRequests', 'AllAwaitingConfirm','Acceptances', 'Rejections',
           'InterviewRequests', 'ArchiveAcceptance', 'ArchiveInterviewRequest', 'ArchiveRejection', 'Applications',
           'SingleApplication', 'accept_and_email', 'reject_and_email', 'request_interview_and_email', 'apply_and_email', 'unapply',
           'clear_application_notifications', 'DeclineAcceptanceAndEmail', 'ConfirmAcceptanceAndEmail', 'AwaitingConfirm']


class AllApplications(EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-applications.html'

    def get_context_data(self, **kwargs):
        context = super(AllApplications, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllAcceptances(EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-acceptances.html'

    def get_context_data(self, **kwargs):
        context = super(AllAcceptances, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllRejections(EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-rejections.html'

    def get_context_data(self, **kwargs):
        context = super(AllRejections, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllInterviewRequests(EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-interviewrequests.html'

    def get_context_data(self, **kwargs):
        context = super(AllInterviewRequests, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context

class AllAwaitingConfirm(EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-awaiting-confirm.html'

    def get_context_data(self, **kwargs):
        context = super(AllAwaitingConfirm, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context

class Acceptances(LoginRequiredMixin, TemplateView):
    template_name = 'applications/acceptances.html'


class Rejections(LoginRequiredMixin, TemplateView):
    template_name = 'applications/rejections.html'


class InterviewRequests(LoginRequiredMixin, TemplateView):
    template_name = 'applications/interview-requests.html'


class AwaitingConfirm(TemplateView):
    template_name = 'applications/awaiting-confirm.html'


class ArchiveAcceptance(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('acceptances')

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))


        if listing.company != self.request.user and self.request.user != user:
            raise PermissionDenied

        if self.request.user.is_employer:
            self.request.user.employer_profile.archive_acceptance(listing, user)
        elif self.request.user.is_student:
            user.profile.archive_acceptance(listing)

        return super().get_redirect_url(*args, **kwargs)


class ArchiveInterviewRequest(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('interview_requests')

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionDenied
        if self.request.user.is_employer:
            self.request.user.employer_profile.archive_interview_request(listing, user)
        elif self.request.user.is_student:
            user.profile.archive_interview_request(listing)
        return super().get_redirect_url(*args, **kwargs)


class ArchiveRejection(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('rejections')

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionDenied
        if self.request.user.is_employer:
            self.request.user.employer_profile.archive_rejection(listing, user)
        elif self.request.user.is_student:
            user.profile.archive_rejection(listing)
        return super().get_redirect_url(*args, **kwargs)

class DeclineAcceptanceAndEmail(RedirectView, StudentRequiredMixin):
    url = reverse_lazy('awaiting_confirm')

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        if not listing.check_if_accepted(self.request.user):
            raise PermissionDenied
        listing.decline_acceptance(self.request.user)
        DeclineAcceptance.declined_acceptance_email(self.request.user, listing)
        return super().get_redirect_url(*args, **kwargs)


class ConfirmAcceptanceAndEmail(RedirectView, StudentRequiredMixin):
    url = reverse_lazy('awaiting_confirm')

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        if not listing.check_if_accepted(self.request.user):
            raise PermissionDenied
        listing.confirm_acceptance(self.request.user)
        ConfirmAcceptance.confirmed_acceptance_email(self.request.user, listing)
        return super().get_redirect_url(*args, **kwargs)

class Applications(LoginRequiredMixin, TemplateView):
    template_name = 'applications/applications.html'


class SingleApplication(LoginRequiredMixin, TemplateView):
    template_name = 'applications/employer/single-application.html'

    def get(self, *args, **kwargs):
        if self.request.user != self.get_listing().company:
            raise PermissionDenied
        return super(SingleApplication, self).get(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['student'] = self.get_student()
        context['listing'] = self.get_listing()
        return context

    def get_student(self):
        return User.objects.get(slug=self.kwargs['user_slug'])

    def get_listing(self):
        return Listing.objects.get(slug=self.kwargs['listing_slug'])    


@login_required
def accept_and_email(request, listing_id, student_id):
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
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionDenied

    student = User.objects.get(id=student_id)
    listing.reject(student_id)
    RejectStudent.reject_student_email(student, listing)
    return render(request, 'success-error/success-rejected-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required
def request_interview_and_email(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionDenied

    student = User.objects.get(id=student_id)
    listing.request_interview(student_id)
    RequestInterview.request_interview_email(student, listing)
    return render(request, 'success-error/success-requested-interview.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required
@student_required
def apply_and_email(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.apply(request.user)
    Applied.applied_email(request.user, listing)
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
@employer_required
def clear_application_notifications(request, slug):
    listing = Listing.objects.get(slug=slug)
    notifs = request.user.notifications.unread()
    notifs = notifs.filter(actor_object_id=listing.id)
    notifs.mark_all_as_deleted()
    return redirect(reverse('applications'))

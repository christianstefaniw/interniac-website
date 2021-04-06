from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, RedirectView

from accounts.models import User
from decorators.student_required import student_required
from marketplace.models import Listing
from mixins.employer_required import EmployerRequiredMixin

__all__ = ['AllApplications', 'AllAcceptances', 'AllRejections', 'AllInterviewRequests', 'Acceptances', 'Rejections',
           'InterviewRequests', 'ArchiveAcceptance', 'ArchiveInterviewRequest', 'ArchiveRejection', 'Applications',
           'SingleApplication', 'accept', 'reject', 'request_interview', 'apply', 'unapply',
           'clear_application_notifications']


class AllApplications(LoginRequiredMixin, EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-applications.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(AllApplications, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllAcceptances(LoginRequiredMixin, EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-acceptances.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(AllAcceptances, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllRejections(LoginRequiredMixin, EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-rejections.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(AllRejections, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class AllInterviewRequests(LoginRequiredMixin, EmployerRequiredMixin, TemplateView):
    template_name = 'applications/employer/all/all-interviewrequests.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(AllInterviewRequests, self).get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(slug=self.kwargs['slug'])
        return context


class Acceptances(LoginRequiredMixin, TemplateView):
    template_name = 'applications/acceptances.html'
    login_url = 'login'


class Rejections(LoginRequiredMixin, TemplateView):
    template_name = 'applications/rejections.html'
    login_url = 'login'


class InterviewRequests(LoginRequiredMixin, TemplateView):
    template_name = 'applications/interview-requests.html'
    login_url = 'login'


class ArchiveAcceptance(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('acceptances')
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))


        if listing.company != self.request.user and self.request.user != user:
            raise PermissionError

        if self.request.user.is_employer:
            self.request.user.employer_profile.archive_acceptance(listing.id, user.id)
        elif self.request.user.is_student:
            user.profile.archive_acceptance(listing.id)

        return super().get_redirect_url(*args, **kwargs)


class ArchiveInterviewRequest(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('interview_requests')
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionError
        if self.request.user.is_employer:
            self.request.user.employer_profile.archive_interview_request(listing.id, user.id)
        elif self.request.user.is_student:
            user.profile.archive_interview_request(listing.id)
        return super().get_redirect_url(*args, **kwargs)


class ArchiveRejection(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('rejections')
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionError
        if self.request.user.is_employer:
            self.request.user.employer_profile.archive_rejection(listing.id, user.id)
        elif self.request.user.is_student:
            user.profile.archive_rejection(listing.id)
        return super().get_redirect_url(*args, **kwargs)


class Applications(LoginRequiredMixin, TemplateView):
    template_name = 'applications/applications.html'
    login_url = 'login'


class SingleApplication(LoginRequiredMixin, TemplateView):
    template_name = 'applications/employer/single-application.html'
    login_url = 'login'

    def get(self, *args, **kwargs):
        if self.request.user != self.get_listing().company:
            raise PermissionError
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


@login_required(login_url='login')
def accept(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionError

    student = User.objects.get(id=student_id)
    listing.accept(student_id)
    return render(request, 'success-error/success-accepted-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required(login_url='login')
def reject(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionError

    student = User.objects.get(id=student_id)
    listing.reject(student_id)
    return render(request, 'success-error/success-rejected-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required(login_url='login')
def request_interview(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionError

    student = User.objects.get(id=student_id)
    listing.request_interview(student_id)
    return render(request, 'success-error/success-requested-interview.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required(login_url='login')
@student_required
def apply(request, listing_id):
    request.user.profile.apply(listing_id)
    redirect_where = request.GET.get('redirect')
    if redirect_where == 'profile':
        return redirect(request.user)
    elif redirect_where == 'success':
        return render(request, 'success-error/success-applied.html',
                      context={'which': Listing.objects.get(id=listing_id)})
    else:
        return HttpResponse(f'<button class="apply-unapply-btn" onclick="unapply({listing_id}, this)">Unapply</button>')


@login_required(login_url='login')
@student_required
def unapply(request, listing_id):
    request.user.profile.unapply(listing_id)
    redirect_where = request.GET.get('redirect')
    if redirect_where == 'profile':
        return redirect('applications')
    elif redirect_where == 'success':
        return render(request, 'success-error/success-unapplied.html',
                      context={'which': Listing.objects.get(id=listing_id)})
    else:
        return HttpResponse(f'<button class="apply-unapply-btn" onclick="apply({listing_id}, this)">Apply</button>')


# TODO create require employer decorator
@login_required(login_url='login')
def clear_application_notifications(request, slug):
    listing = Listing.objects.get(slug=slug)
    notifs = request.user.notifications.unread()
    notifs = notifs.filter(actor_object_id=listing.id)
    for _, i in enumerate(notifs):
        i.mark_as_read()
    return redirect(reverse('applications'))

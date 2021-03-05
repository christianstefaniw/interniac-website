from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from accounts.models import User
from marketplace.models import Listing


class Acceptances(LoginRequiredMixin, TemplateView):
    template_name = 'applications/acceptances.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class Rejections(LoginRequiredMixin, TemplateView):
    template_name = 'applications/rejections.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class ArchiveAcceptance(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('acceptances')
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionError
        listing.acceptances.remove(user)
        return super().get_redirect_url(*args, **kwargs)


class ArchiveInterviewRequest(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('interview_requests')
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionError
        listing.interview_requests.remove(user)
        return super().get_redirect_url(*args, **kwargs)


class InterviewRequests(LoginRequiredMixin, TemplateView):
    template_name = 'applications/interview-requests.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArchiveRejection(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('rejections')
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('listing_id'))
        user = User.objects.get(id=self.kwargs.get('student_id'))
        if listing.company != self.request.user and self.request.user != user:
            raise PermissionError
        listing.rejections.remove(user)
        return super().get_redirect_url(*args, **kwargs)


class Applications(LoginRequiredMixin, TemplateView):
    template_name = 'applications/applications.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_student:
            pass
        return context


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
    listing.acceptances.add(student)
    listing.applications.remove(student)
    listing.accept_email(student)
    return render(request, 'success-error/success-accepted-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required(login_url='login')
def reject(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionError

    student = User.objects.get(id=student_id)
    listing.rejections.add(student)
    listing.applications.remove(student)
    listing.reject_email(student)
    return render(request, 'success-error/success-rejected-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


@login_required(login_url='login')
def request_interview(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user != listing.company:
        raise PermissionError

    student = User.objects.get(id=student_id)
    listing.interview_requests.add(student)
    listing.request_interview_email(student)
    return render(request, 'success-error/success-requested-interview.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})

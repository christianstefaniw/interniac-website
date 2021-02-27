from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.models import User
from marketplace.models import Listing


class Applications(TemplateView):
    template_name = 'applications/applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_student:
            pass
        elif self.request.user.is_employer:
            context['listings'] = self.get_listings()
        return context

    def get_listings(self):
        return Listing.objects.filter(company=self.request.user)


class SingleApplication(TemplateView):
    template_name = 'applications/single-application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['student'] = self.get_student()
        context['listing'] = self.get_listing()
        return context

    def get_student(self):
        return User.objects.get(slug=self.kwargs['user_slug'])

    def get_listing(self):
        return Listing.objects.get(slug=self.kwargs['listing_slug'])


def accept(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)
    student = User.objects.get(id=student_id)
    listing.acceptances.add(student)
    listing.applications.remove(student)
    listing.accept_email(student)
    return render(request, 'success-error/success-accepted-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})


def reject(request, listing_id, student_id):
    listing = Listing.objects.get(id=listing_id)
    student = User.objects.get(id=student_id)
    listing.rejections.add(student)
    listing.applications.remove(student)
    listing.reject_email(student)
    return render(request, 'success-error/success-rejected-student.html',
                  context={'first': student.first_name, 'last': student.last_name, 'listing_title': listing.title})

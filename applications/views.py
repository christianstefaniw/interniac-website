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
        if self.request.user.is_employer:
            context['listings'] = self.get_listings()
        return context

    def get_listings(self):
        return Listing.objects.filter(org__email=self.request.user.email)


class SingleApplication(TemplateView):
    template_name = 'applications/single-application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.get_user()
        return context

    def get_user(self):
        return User.objects.get(id=self.kwargs['id'])


def accept(request):
    listing = Listing.objects.get(id=request.GET.get('listing_id'))
    student = User.objects.get(id=request.GET.get('student_id'))
    listing.acceptances.add(student)
    listing.applications.remove(student)
    return render(request, 'success-error/success-accepted-student.html',
                  context={'first': student.first_name, 'last': student.last_name})


def reject(request):
    listing = Listing.objects.get(id=request.GET.get('listing_id'))
    student = User.objects.get(id=request.GET.get('student_id'))
    listing.rejections.add(student)
    listing.applications.remove(student)
    return render(request, 'success-error/success-rejected-student.html',
                  context={'first': student.first_name, 'last': student.last_name})

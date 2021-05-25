from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from accounts.models import User
from .forms import ContactForm, EmailForm
from .models import Event


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contact_form'] = ContactForm()
        context['newsletter_form'] = EmailForm()
        context['events'] = Event.objects.all()[:3]
        context['students'] = User.objects.filter(is_student=True).count()
        context['employers'] = User.objects.filter(is_employer=True).count()
        return context

    def post(self, request, **kwargs):

        if 'email_signup' in self.request.POST:
            form = EmailForm(request.POST)
            if form.is_valid():
                return redirect('success')
            return redirect('error')

        if 'message' in self.request.POST:
            form = ContactForm(request.POST)
            if form.is_valid():
                form.send_email()
                return redirect('success')
            return redirect('error')


def read_more(request, pk):
    return render(request, 'read-more.html', {'event': Event.objects.get(id=pk)})

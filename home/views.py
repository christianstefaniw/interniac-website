from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import ContactForm, EmailForm
from .models import Statistics, Event


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contact_form'] = ContactForm()
        context['email_form'] = EmailForm()
        context['stats'] = Statistics.objects.all()
        context['events'] = Event.objects.all()[:3]
        return context

    def post(self, request, *args, **kwargs):
        if 'email_signup' in self.request.POST:
            form = EmailForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/success')
            else:
                return HttpResponseRedirect('/error')


def read_more(request, pk):
    return render(request, 'read-more.html', {'event': Event.objects.get(id=pk)})

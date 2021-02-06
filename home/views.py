from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from .forms import ContactForm, EmailForm


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contact_form'] = ContactForm()
        context['email_form'] = EmailForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'email_signup' in self.request.POST:
            form = EmailForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/success')
            else:
                return HttpResponseRedirect('/error')

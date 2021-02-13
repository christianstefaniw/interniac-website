from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from accounts.models import User
from .email import subscribed_email, send_email
from .forms import ContactForm, EmailForm
from .models import Event, EmailSignup


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contact_form'] = ContactForm()
        context['email_form'] = EmailForm()
        context['events'] = Event.objects.all()[:3]
        context['students'] = User.objects.filter(is_student=True).count()
        context['employers'] = User.objects.filter(is_employer=True).count()
        context['professionals'] = 0
        return context

    def post(self, request, *args, **kwargs):

        if 'email_signup' in self.request.POST:
            form = EmailForm(request.POST)

            if form.is_valid():
                if EmailSignup.objects.filter(email_signup=form.cleaned_data['email_signup']).exists():
                    return HttpResponseRedirect('/success')
                form.save()
                subscribed_email(form)
                return HttpResponseRedirect('/success')
            else:
                return HttpResponseRedirect('/error')

        if 'message' in self.request.POST:
            form = ContactForm(request.POST)

            if form.is_valid():
                send_email(form)
                return redirect('/success')
            else:
                return redirect('/error')


def read_more(request, pk):
    return render(request, 'read-more.html', {'event': Event.objects.get(id=pk)})


def unsubscribe(request, email):
    try:
        EmailSignup.objects.get(email_signup=email).delete()
        return redirect('success')
    except:
        return redirect('error')



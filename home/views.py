from django.views.generic import TemplateView
from django.shortcuts import render

from .forms import ContactForm


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = ContactForm()
        return context


def Error404Handler(request):
    return render(request, '404.html')

from django.views.generic import TemplateView
from django.shortcuts import render


class HomePage(TemplateView):
    template_name = 'index.html'


def Error404Handler(request):
    return render(request, '404.html')

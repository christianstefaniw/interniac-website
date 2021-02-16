from django import views
from django.shortcuts import render


def success(request):
    return render(request, 'success-error/success-home.html')


def error(request):
    return render(request, 'success-error/error-home.html')


def Error404Handler(request):
    return render(request, '404.html')

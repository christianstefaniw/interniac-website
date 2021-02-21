from django.shortcuts import render


def success(request):
    return render(request, 'success-error/success-general.html')


def error(request):
    return render(request, 'success-error/error-general.html')


def Error404Handler(request):
    return render(request, '404.html')


def Error500Handler(request):
    return render(request, 'success-error/error-general.html')

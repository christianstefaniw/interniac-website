from django.shortcuts import render

from accounts.models import User


def success(request):
    return render(request, 'success-error/success-general.html')


def error(request):
    return render(request, 'success-error/error-general.html')


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


def num_students(request):
    return User.objects.filter(is_student=True).count()


def num_employers(request):
    return User.objects.filter(is_employer=True).count()

from django.http import JsonResponse

from accounts.models import User


def num_students(request):
    response_data = {
        'label': 'students',
        'message': User.objects.filter(is_student=True).count()
    }
    return JsonResponse(response_data)


def num_employers(request):
    response_data = {
        'label': 'employers',
        'message': User.objects.filter(is_employer=True).count()
    }
    return JsonResponse(response_data)

from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

from accounts.models import User


def num_students(request):
    return HttpResponse(User.objects.filter(is_student=True).count())


def num_employers(requst):
    return HttpResponse(User.objects.filter(is_employer=True).count())

from django.urls import path

from stats.views import num_employers, num_students


urlpatterns = [
    path('num-students/', num_students),
    path('num-employers/', num_employers),
]

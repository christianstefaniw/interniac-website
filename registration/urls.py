from django.urls import path, include

from .views import *

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]

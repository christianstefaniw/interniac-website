from django.urls import path, include
from django.contrib.auth import views as auth_views

from accounts.views import profile

urlpatterns = [
    path('profile/', profile, name='profile')
]

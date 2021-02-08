from django.urls import path, include
from django.contrib.auth import views as auth_views

from accounts.views import Profile

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile')
]

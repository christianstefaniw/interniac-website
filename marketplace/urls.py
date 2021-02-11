from django.urls import path

from .views import marketplace

urlpatterns = [
    path('', marketplace, name='marketplace'),
]

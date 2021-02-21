from django.urls import path

from .views import accept, reject, Applications, SingleApplication


urlpatterns = [
    path('accept/', accept, name='accept'),
    path('reject/', reject, name='reject'),
    path('application/<slug:slug>', SingleApplication.as_view(), name='single_application'),
    path('', Applications.as_view(), name='applications')
]

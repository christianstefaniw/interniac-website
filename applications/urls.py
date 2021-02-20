from django.urls import path

from .views import accept, Applications, SingleApplication


urlpatterns = [
    path('acceptstudent/', accept, name='accept'),
    path('application/<int:id>', SingleApplication.as_view(), name='single_application'),
    path('', Applications.as_view(), name='applications')
]

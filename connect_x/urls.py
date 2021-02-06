from django.contrib import admin
from django.urls import path, include

from .views import *
from home import urls as home_urls
from careers.views import CareersPage
from students.views import StudentsPage
from employers.views import EmployersPage
from aboutus.views import AboutUsPage

urlpatterns = [
    path('', include(home_urls)),
    path('careers/', CareersPage.as_view(), name='careers'),
    path('students/', StudentsPage.as_view(), name='students'),
    path('employers/', EmployersPage.as_view(), name='employers'),
    path('aboutus/', AboutUsPage.as_view(), name='aboutus'),
    path('success/', success, name='success'),
    path('error/', error, name='error'),
    path('admin/', admin.site.urls),
]

handler500 = 'connect_x.views.Error404Handler'


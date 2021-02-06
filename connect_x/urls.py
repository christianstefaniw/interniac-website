from django.contrib import admin
from django.urls import path

from .views import HomePage
from careers.views import CareersPage
from students.views import StudentsPage
from employers.views import EmployersPage
from aboutus.views import AboutUsPage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('careers/', CareersPage.as_view(), name='careers'),
    path('students/', StudentsPage.as_view(), name='students'),
    path('employers/', EmployersPage.as_view(), name='employers'),
    path('aboutus/', AboutUsPage.as_view(), name='aboutus'),
    path('admin/', admin.site.urls),
]

handler500 = 'connect_x.views.Error404Handler'


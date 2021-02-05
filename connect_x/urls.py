from django.contrib import admin
from django.urls import path
from django.views import defaults

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('admin/', admin.site.urls),
]

handler500 = 'connect_x.views.Error404Handler'


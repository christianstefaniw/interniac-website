from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('admin/', admin.site.urls),
]

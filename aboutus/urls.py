from django.urls import path

from .views import AboutUsPage


urlpatterns = [
    path('', AboutUsPage.as_view(), name='aboutus')
]

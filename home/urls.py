from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('readmore/<int:pk>', read_more, name='read_more')
]
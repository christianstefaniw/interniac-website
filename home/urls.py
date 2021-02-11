from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('unsubscribe/<str:email>', unsubscribe, name='unsubscribe'),
    path('readmore/<int:pk>', read_more, name='read_more')
]

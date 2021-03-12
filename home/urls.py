from django.urls import path

from .views import HomePage, read_more

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('readmore/<int:pk>', read_more, name='read_more')
]

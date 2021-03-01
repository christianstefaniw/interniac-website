from django.urls import path

from accounts.views import *


urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('delete/', delete_user, name='delete'),
    path('listings/', Listings.as_view(), name='listings')
]

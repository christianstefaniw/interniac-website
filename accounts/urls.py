from django.urls import path

from .views import Profile, Listings, delete_user


urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('delete/', delete_user, name='delete'),
    path('listings/', Listings.as_view(), name='listings')
]

from django.urls import path

from .views import Profile, Listings, delete_user

"""
`urlpatterns` for the accounts app  
Currently we support the following 3 urls:

1. **`profile`** - view current user's account
2. **`delete`** - delete current user's
3. **`listings`** - view current user's posted listings (only for employers)

"""
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('delete/', delete_user, name='delete'),
    path('listings/', Listings.as_view(), name='listings')
]

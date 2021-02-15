from django.urls import path

from accounts.views import Profile, unapply

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('unapply/<int:listing_id>', unapply, name='unapply')
]

from django.urls import path

from accounts.views import Profile, apply, unapply, delete

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('apply/<int:listing_id>', apply, name='apply-profile'),
    path('unapply/<int:listing_id>', unapply, name='unapply-profile'),
    path('delete/<int:id>', delete, name='delete'),
]

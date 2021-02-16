from django.urls import path

from .views import Marketplace, CreateListing, FilterListings, apply, unapply

urlpatterns = [
    path('', Marketplace.as_view(), name='marketplace'),
    path('createlisting/', CreateListing.as_view(), name='createlisting'),
    path('filter/', FilterListings.as_view(), name='filter'),
    path('apply/<int:listing_id>', apply, name='apply'),
    path('unapply/<int:listing_id>', unapply, name='unapply'),
]

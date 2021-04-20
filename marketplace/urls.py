from django.urls import path

from .views import *

urlpatterns = [
    path('', Marketplace.as_view(), name='marketplace'),
    path('createlisting/', CreateListing.as_view(), name='createlisting'),
    path('filter/', FilterListings.as_view(), name='filter'),
    path('listing/<slug:slug>', ViewListing.as_view(), name='listing'),
    path('delete/<int:listing_id>', delete_listing, name='delete_listing'),
    path('editlisting/<slug:slug>/', EditListing.as_view(), name='edit_listing')
]

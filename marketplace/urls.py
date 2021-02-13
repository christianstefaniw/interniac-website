from django.urls import path

from .views import Marketplace, CreateListing

urlpatterns = [
    path('', Marketplace.as_view(), name='marketplace'),
    path('createlisting/', CreateListing.as_view(), name='createlisting')
]

from django.urls import path

from .views import accept, reject, Applications, SingleApplication


urlpatterns = [
    path('accept/<int:listing_id>/<int:student_id>', accept, name='accept'),
    path('reject/<int:listing_id>/<int:student_id>', reject, name='reject'),
    path('application/<slug:listing_slug>/<slug:user_slug>', SingleApplication.as_view(), name='single_application'),
    path('', Applications.as_view(), name='applications')
]

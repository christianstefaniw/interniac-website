from django.urls import path

from .views import *


urlpatterns = [
    path('accept/<int:listing_id>/<int:student_id>', accept, name='accept'),
    path('reject/<int:listing_id>/<int:student_id>', reject, name='reject'),
    path('application/<slug:listing_slug>/<slug:user_slug>', SingleApplication.as_view(), name='single_application'),
    path('acceptances', Acceptances.as_view(), name='acceptances'),
    path('rejections', Rejections.as_view(), name='rejections'),
    path('archiveaccepted/<int:listing_id>/<int:student_id>', ArchiveAcceptance.as_view(), name='archive_accepted'),
    path('archiverejected/<int:listing_id>/<int:student_id>', ArchiveRejection.as_view(), name='archive_rejected'),
    path('', Applications.as_view(), name='applications')
]

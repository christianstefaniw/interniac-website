from django.urls import path

from .views import *

urlpatterns = [
    path('apply/<int:listing_id>', apply, name='apply'),
    path('unapply/<int:listing_id>', unapply, name='unapply'),
    path('accept/<int:listing_id>/<int:student_id>', accept, name='accept'),
    path('reject/<int:listing_id>/<int:student_id>', reject, name='reject'),
    path('request_interview/<int:listing_id>/<int:student_id>', request_interview, name='request_interview'),
    path('application/<slug:listing_slug>/<slug:user_slug>', SingleApplication.as_view(), name='single_application'),
    path('acceptances', Acceptances.as_view(), name='acceptances'),
    path('rejections', Rejections.as_view(), name='rejections'),
    path('interviewrequests', InterviewRequests.as_view(), name='interview_requests'),
    path('archiveaccepted/<int:listing_id>/<int:student_id>', ArchiveAcceptance.as_view(), name='archive_accepted'),
    path('archiverejected/<int:listing_id>/<int:student_id>', ArchiveRejection.as_view(), name='archive_rejected'),
    path('archiveinterviewrequest/<int:listing_id>/<int:student_id>', ArchiveInterviewRequest.as_view(),
         name='archive_interview_request'),
    path('all/applications/<slug:slug>', AllApplications.as_view(), name='all_applications'),
    path('all/rejections/<slug:slug>', AllRejections.as_view(), name='all_rejections'),
    path('all/acceptances/<slug:slug>', AllAcceptances.as_view(), name='all_acceptances'),
    path('all/interviewrequests/<slug:slug>', AllInterviewRequests.as_view(), name='all_interviewrequests'),
    path('clearnotifs/<slug:slug>', clear_application_notifications, name='clear_notifs'),
    path('', Applications.as_view(), name='applications')
]

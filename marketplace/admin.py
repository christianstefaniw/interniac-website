from django.contrib import admin

from .models import Listing, Career


class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ['applications', 'acceptances', 'rejections', 'interview_requests', 'employer_acceptances', 'employer_rejections', 'employer_interview_requests',
                         'student_acceptances', 'student_rejections', 'student_interview_requests', 'awaiting_confirm_acceptance', 'already_applied'
                         ]


admin.site.register(Listing, ListingAdmin)
admin.site.register(Career)

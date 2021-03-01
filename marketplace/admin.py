from django.contrib import admin

from .models import Listing, Career


class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ['applications', 'acceptances', 'rejections', 'interview_requests']


admin.site.register(Listing, ListingAdmin)
admin.site.register(Career)

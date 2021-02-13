from django.contrib import admin

from .models import *


class StatsAdmin(admin.ModelAdmin):
    list_display = ('students', 'employers', 'professionals')


admin.site.register(EmailSignup)
admin.site.register(Event)

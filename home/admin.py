from django.contrib import admin

from .models import Event


class StatsAdmin(admin.ModelAdmin):
    list_display = ('students', 'employers', 'professionals')


admin.site.register(Event)

from django.contrib import admin
from .models import StudentProfile, EmployerProfile, User

"""
Register models to the Django admin interface
"""
admin.site.register(StudentProfile)
admin.site.register(EmployerProfile)
admin.site.register(User)

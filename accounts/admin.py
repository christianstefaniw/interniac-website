from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from accounts.models import StudentProfile

admin.site.register(StudentProfile)
admin.site.register(User, UserAdmin)

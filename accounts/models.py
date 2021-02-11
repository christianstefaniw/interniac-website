from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    username = models.CharField(max_length=256, unique=False, blank=True)
    email = models.EmailField(max_length=256, unique=True, blank=False)
    is_student = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    phone = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    hs = models.CharField(max_length=20, null=True, blank=True)
    hs_addy = models.CharField(max_length=20, null=True, blank=True)
    teacher_or_counselor_email = models.EmailField(null=True, blank=True)
    teacher_or_counselor_name = models.CharField(max_length=30, null=True, blank=True)
    awards_achievements = models.TextField(null=True, blank=True)
    work_exp = models.TextField(null=True, blank=True)
    volunteering_experience = models.TextField(null=True, blank=True)
    extracurriculars = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    leadership_roles = models.TextField(null=True, blank=True)
    link1 = models.URLField(null=True, blank=True)
    link2 = models.URLField(null=True, blank=True)
    link3 = models.URLField(null=True, blank=True)
    link4 = models.URLField(null=True, blank=True)

    def __str__(self):
        return "%s's profile" % self.user

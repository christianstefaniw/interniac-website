from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    awards_achievements = models.CharField(max_length=30, null=True)
    work_exp = models.CharField(max_length=30, null=True)
    teacher_or_counselor_email = models.EmailField(null=True)
    teacher_or_counselor_name = models.CharField(max_length=30, null=True)
    volunteers = models.CharField(max_length=30, null=True)
    dob = models.DateField(null=True)
    hs_addy = models.CharField(max_length=20, null=True)
    extracurriculars = models.CharField(max_length=30, null=True)
    phone = models.IntegerField(null=True)
    skills = models.CharField(max_length=30, null=True)
    hs = models.CharField(max_length=20, null=True)
    leadership_roles = models.CharField(max_length=30, null=True)

    def __str__(self):
        return "%s's profile" % self.user

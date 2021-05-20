from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django_unique_slugify import unique_slugify
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField

from accounts.managers import UserManager
from connect_x.settings import DEBUG

"""
Models for the accounts application  
Currently we support the following 3 models:

1. **`User`** - custum user model
2. **`EmployerProfile`** - additional account info for employer user
3. **`StudentProfile`** - additional account info for student user

"""

class User(AbstractUser):
    """Custom User model, inherits from the basic user model"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    username = models.CharField(max_length=256, unique=False, blank=True)
    email = models.EmailField(max_length=256, unique=True, blank=False)
    if DEBUG:
        profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.png',
                                            null=True, blank=True)
    else:
        profile_picture = CloudinaryField(
            'Profile picture', default='default_aze1tf.png')
    is_student = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    slug = models.SlugField(max_length=256, unique=False, blank=True)

    def get_absolute_url(self):
        return reverse('profile')

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_profile_pic_url(self):
        return self.profile_picture.url

    def __str__(self):
        if self.is_employer:
            if self.employer_profile.company_name is not None:
                return self.employer_profile.company_name
            else:
                return self.email
        else:
            return self.email


class EmployerProfile(models.Model):
    """
    Profile for employer user, meant to contain extra data specific to employers.  
    This model will be related to a `User` instance if the `is_employer` field set to True.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='employer_profile')
    company_name = models.CharField(max_length=50, unique=False, blank=False)
    company_website = models.URLField(blank=True)

    def slug_employer(self):
        """Unique slugify related `User` instance with company's name"""

        self.user.slug = f"{self.company_name}"
        unique_slugify(self.user, self.user.slug)

    def archive_interview_request(self, listing, user):
        listing.employer_interview_requests.remove(user)

    def archive_acceptance(self, listing, user):
        listing.employer_acceptances.remove(user)

    def archive_rejection(self, listing, user):
        listing.employer_rejections.remove(user)

    def __str__(self):
        return self.company_name


class StudentProfile(models.Model):
    """
    Profile for student user, meant to contain extra data specific to students.  
    This model will be related to a `User` instance if the `is_student` field set to True.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    phone = PhoneNumberField(blank=True, null=True, unique=True)
    dob = models.DateField(null=True, blank=True)
    hs = models.CharField(max_length=100, null=True, blank=True)
    hs_addy = models.CharField(max_length=100, null=True, blank=True)
    teacher_or_counselor_email = models.EmailField(null=True, blank=True)
    teacher_or_counselor_name = models.CharField(
        max_length=100, null=True, blank=True)
    awards_achievements = models.TextField(null=True, blank=True)
    work_exp = models.TextField(null=True, blank=True)
    volunteering_exp = models.TextField(null=True, blank=True)
    extracurriculars = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    leadership_roles = models.TextField(null=True, blank=True)
    link1 = models.URLField(null=True, blank=True)
    link2 = models.URLField(null=True, blank=True)
    link3 = models.URLField(null=True, blank=True)
    link4 = models.URLField(null=True, blank=True)

    def slug_student(self):
        """Unique slugify related `User` instance with student's full name"""

        self.user.slug = self.user.get_full_name
        unique_slugify(self.user, self.user.slug)

    def archive_interview_request(self, listing):
        """
        Archive an interview request for a listing specified for this student

        @type listing: `Listing`  
        @param listing: the listing that this student was requested an interview for
        """

        listing.archive_interview_request(self.user)

    def archive_acceptance(self, listing):
        """
        Archive an acceptance for a listing specified for this user

        @type listing: `Listing`  
        @param listing: the listing that this student was accepted to
        """

        listing.archive_student_acceptance(self.user)

    def archive_rejection(self, listing):
        """
        Archive a rejection for a listing specified for this user

        @type listing: `Listing`  
        @param listing: the listing that this student was accepted to
        """

        listing.archive_student_rejection(self.user)

    def summarize(self):
        data = {
            'email': self.user.email,
            'profile picture': self.user.get_profile_pic_url,
            'is student': self.user.is_student,
            'is employer': self.user.is_employer,
            'slug': self.user.slug,
            'dob': self.dob,
            'high school': self.hs,
            'high school address': self.hs_addy,
            'teacher or counselor email': self.teacher_or_counselor_email,
            'teacher or counselor name': self.teacher_or_counselor_name,
            'awards and achievements': self.awards_achievements,
            'work experience': self.work_exp,
            'volunteer experience': self.volunteering_exp,
            'extracurriculars': self.extracurriculars,
            'skills': self.skills,
            'leadership roles': self.leadership_roles,
            'link 1': self.link1,
            'link 2': self.link2,
            'link 3': self.link3,
            'link 4': self.link4
        }
        return data

    def __str__(self):
        return f"{self.user.first_name}'s profile"

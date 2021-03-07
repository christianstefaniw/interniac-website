import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_unique_slugify import unique_slugify
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import UserManager
from marketplace.models import Listing


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    username = models.CharField(max_length=256, unique=False, blank=True)
    email = models.EmailField(max_length=256, unique=True, blank=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.png',
                                        null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    slug = models.SlugField(max_length=256, unique=False, blank=True)

    def get_absolute_url(self):
        return reverse('profile')

    def slug_employer(self):
        self.slug = f"{self.employer_profile.company_name}"
        unique_slugify(self, self.slug)
        self.save()

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def slug_student(self):
        self.slug = self.get_full_name
        unique_slugify(self, self.slug)
        self.save()

    @property
    def get_profile_pic_url(self):
        return self.profile_picture.url

    def summarize(self):
        data = {
            'email': self.email,
            'profile picture': self.get_profile_pic_url,
            'is student': self.is_student,
            'is employer': self.is_employer,
            'slug': self.slug,
            'dob': self.profile.dob,
            'high school': self.profile.hs,
            'high school address': self.profile.hs_addy,
            'teacher or counselor email': self.profile.teacher_or_counselor_email,
            'teacher or counselor name': self.profile.teacher_or_counselor_name,
            'awards and achievements': self.profile.awards_achievements,
            'work experience': self.profile.work_exp,
            'volunteer experience': self.profile.volunteering_exp,
            'extracurriculars': self.profile.extracurriculars,
            'skills': self.profile.skills,
            'leadership roles': self.profile.leadership_roles,
            'link 1': self.profile.link1,
            'link 2': self.profile.link2,
            'link 3': self.profile.link3,
            'link 4': self.profile.link4
        }
        return data

    def __str__(self):
        if self.is_employer:
            if self.employer_profile.company_name is not None:
                return self.employer_profile.company_name
            else:
                return self.email
        else:
            return self.email


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employer_profile')
    company_name = models.CharField(max_length=30, unique=False, blank=True)
    company_website = models.URLField(blank=True)

    def archive_interview_request(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        self.user.employer_interview_requests.remove(listing)

    def archive_acceptance(self, listing_id, user_id):
        listing = Listing.objects.get(id=listing_id)
        listing.employer_acceptances.remove(User.objects.get(id=user_id))

    def archive_rejection(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        self.user.employer_rejections.remove(listing)

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        return super(EmployerProfile, self).delete(using=None, keep_parents=False)

    def __str__(self):
        return self.company_name


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    phone = PhoneNumberField(blank=True, null=True, unique=True)
    dob = models.DateField(null=True, blank=True)
    hs = models.CharField(max_length=20, null=True, blank=True)
    hs_addy = models.CharField(max_length=20, null=True, blank=True)
    teacher_or_counselor_email = models.EmailField(null=True, blank=True)
    teacher_or_counselor_name = models.CharField(max_length=30, null=True, blank=True)
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

    def reject(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        listing.applications.remove(self.user)
        listing.rejections.add(self.user)
        listing.company.employer_rejections.add(listing)
        listing.reject_email(self.user)
        self.user.student_rejections.add(listing)
        if self.user in listing.interview_requests.all():
            listing.interview_requests.remove(self.user)

    def request_interview(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        listing.interview_requests.add(self.user)
        listing.company.employer_interview_requests.add(self.user)
        self.user.student_interview_requests.add(listing)
        listing.request_interview_email(self.user)

    def archive_interview_request(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        self.user.student_interview_requests.remove(listing)

    def archive_acceptance(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        listing.student_acceptances.remove(self.user)

    def archive_rejection(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        self.user.student_rejections.remove(listing)

    def apply(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        listing.applications.add(self.user)

    def unapply(self, listing_id):
        listing = Listing.objects.get(id=listing_id)
        listing.applications.remove(self.user)

    def __str__(self):
        return f"{self.user.first_name}'s profile"


# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.profile_picture:
        if instance.profile_picture.name == 'profile_pictures/default.png':
            return
        elif os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = User.objects.get(pk=instance.pk).profile_picture
    except User.DoesNotExist:
        return False

    new_file = instance.profile_picture
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

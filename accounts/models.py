import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_unique_slugify import unique_slugify

from accounts.managers import UserManager


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
    slug = models.SlugField(max_length=256, unique=True, blank=True)
    company_name = models.CharField(max_length=30, unique=False, blank=True)

    def get_absolute_url(self):
        return reverse('profile')

    def save(self, *args, **kwargs):
        if self.is_employer:
            self.slug = f"{self.company_name}"
        else:
            self.slug = f"{self.first_name} {self.last_name}"
        unique_slugify(self, self.slug)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        if self.is_employer:
            return self.company_name
        else:
            return self.email


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, related_name='employer_profile')
    company_website = models.URLField(blank=True)

    def __str__(self):
        return self.user.company_name


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, related_name='profile')
    phone = models.IntegerField(null=True, blank=True)
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
        if os.path.isfile(instance.profile_picture.path):
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

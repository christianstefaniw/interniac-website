import os

from django.dispatch import receiver
from django.db import models

from .models import User, StudentProfile, EmployerProfile


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            instance.slug_student()
            StudentProfile.objects.create(user=instance)
        elif instance.is_employer:
            instance.slug_employer()
            EmployerProfile.objects.create(user=instance)
        instance.save()
            

@receiver(models.signals.post_delete, sender=EmployerProfile)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()


@receiver(models.signals.post_delete, sender=StudentProfile)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()


@receiver(models.signals.pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.is_student:
        instance.profile.delete()
    elif instance.is_employer:
        instance.employer_profile.delete()


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.profile_picture:
        if instance.profile_picture.name == 'profile_pictures/default.png':
            return
        elif os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
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

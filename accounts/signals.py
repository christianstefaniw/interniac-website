from django.dispatch import receiver
from django.db import models

from .models import User, StudentProfile, EmployerProfile


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
            instance.slug_student()
        elif instance.is_employer:
            EmployerProfile.objects.create(user=instance)
            instance.slug_employer()
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

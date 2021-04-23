from django.dispatch import receiver
from django.db import models

from .models import User, StudentProfile, EmployerProfile

'''Creates and attached a profile to a newly created user instance'''
@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        elif instance.is_employer:
            EmployerProfile.objects.create(user=instance)

'''Slugifies a'''
@receiver(models.signals.post_save, sender=EmployerProfile)
def slug_employer(sender, instance, created, **kwargs):
    # TODO make it so instance doesn't reslug when dependent fields aren't updated
    if created:
        return
    instance.slug_employer()
    instance.user.save()

@receiver(models.signals.post_save, sender=StudentProfile)
def slug_student(sender, instance, created, **kwargs):
    # TODO make it so instance doesn't reslug when dependent fields aren't updated
    if created:
        return
    
    instance.slug_student()
    instance.user.save()

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

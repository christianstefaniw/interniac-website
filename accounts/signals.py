from django.dispatch import receiver
from django.db import models

from .models import User, StudentProfile, EmployerProfile

@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''Signal receiver that creates and attached a profile to a newly created user instance'''

    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        elif instance.is_employer:
            EmployerProfile.objects.create(user=instance)

@receiver(models.signals.post_save, sender=EmployerProfile)
def slug_employer(sender, instance, created, **kwargs):
    '''Signal receiver that slugifies a user employer instance'''

    # TODO make it so instance doesn't reslug when dependent fields aren't updated
    if created:
        return
    instance.slug_employer()
    instance.user.save()

@receiver(models.signals.post_save, sender=StudentProfile)
def slug_student(sender, instance, created, **kwargs):
    '''Signal receiver that slugifies a user student instance'''

    # TODO make it so instance doesn't reslug when dependent fields aren't updated
    if created:
        return
    
    instance.slug_student()
    instance.user.save()

@receiver(models.signals.post_delete, sender=EmployerProfile)
def delete_user(sender, instance, **kwargs):
    '''delete related user instance when employer profile instance is deleted'''
    instance.user.delete()


@receiver(models.signals.post_delete, sender=StudentProfile)
def delete_user(sender, instance, **kwargs):
    '''delete related user instance when student profile instance is deleted'''
    instance.user.delete()


@receiver(models.signals.pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    '''delete related profile instance when user instance is deleted'''
    if instance.is_student:
        instance.profile.delete()
    elif instance.is_employer:
        instance.employer_profile.delete()

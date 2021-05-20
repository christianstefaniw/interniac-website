from django.dispatch import receiver
from django.db import models

from .models import User, StudentProfile, EmployerProfile


"""
Signals for the accounts application  
Currently we support the following 6 signals:

1. **`create_profile`** - creates profile for a certian user
2. **`slug_employer`** - slugifies a employer user
3. **`slug_student`** - slugifies a student user
4. **`delete_employer_user`** - delete related user upon employer profile delete
5. **`delete_student_user`** - delete related user upon student profile delete
6. **`delete_profile`** - delete related profile upon user delete

"""


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Signal receiver that creates and attached a profile to a newly created user instance"""

    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
            instance.save()
        elif instance.is_employer:
            EmployerProfile.objects.create(user=instance)


@receiver(models.signals.post_save, sender=EmployerProfile)
def slug_employer(sender, instance, created, **kwargs):
    """Signal receiver that slugifies a user employer instance"""

    instance.slug_employer()
    instance.user.save()


@receiver(models.signals.post_save, sender=StudentProfile)
def slug_student(sender, instance, created, **kwargs):
    """Signal receiver that slugifies a user student instance"""

    instance.slug_student()
    instance.user.save()


@receiver(models.signals.post_delete, sender=EmployerProfile)
def delete_employer_user(sender, instance, **kwargs):
    """Delete related user instance when employer profile instance is deleted"""
    instance.user.delete()


@receiver(models.signals.post_delete, sender=StudentProfile)
def delete_student_user(sender, instance, **kwargs):
    """Delete related user instance when student profile instance is deleted"""
    instance.user.delete()


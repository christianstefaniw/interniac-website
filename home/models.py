import os

from django.db import models
from django.dispatch import receiver


class Event(models.Model):
    datetime = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.TextField()
    meet_url = models.URLField()
    img = models.ImageField(upload_to="events")

    def __str__(self):
        return self.name


# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=Event)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


@receiver(models.signals.pre_save, sender=Event)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Event.objects.get(pk=instance.pk).img
    except Event.DoesNotExist:
        return False

    new_file = instance.img
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

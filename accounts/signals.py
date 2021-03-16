import os

from django.dispatch import receiver, Signal
from django.db import models

from .models import User

clear_notifs_signal = Signal(providing_args=["listing"])


@receiver(clear_notifs_signal)
def clear(sender, listing, **kwargs):
    notifs = sender.notifications.unread()
    notifs = notifs.filter(actor_object_id=listing.id)
    for _, i in enumerate(notifs):
        i.mark_as_read()


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

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_unique_slugify import unique_slugify

from marketplace.models import Listing

@receiver(post_save, sender=Listing)
def slugify(sender, instance, created, **kwargs):
    if created:
        instance.slug = instance.title
        unique_slugify(instance, instance.slug)
        instance.save()

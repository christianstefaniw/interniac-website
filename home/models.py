import os
from cloudinary.models import CloudinaryField

from django.db import models
from django.dispatch import receiver


class Event(models.Model):
    datetime = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.TextField()
    meet_url = models.URLField()
    img = CloudinaryField('Image', default='logo-small_zxmfbe.png')

    def __str__(self):
        return self.name

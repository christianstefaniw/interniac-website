from cloudinary.models import CloudinaryField

from django.db import models

from connect_x.settings import DEBUG

class Event(models.Model):
    datetime = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.TextField()
    meet_url = models.URLField()
    if DEBUG:
        img = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.png',
                                        null=True, blank=True)
    else:
        img = CloudinaryField('Image', default='logo-small_zxmfbe.png')

    def __str__(self):
        return self.name

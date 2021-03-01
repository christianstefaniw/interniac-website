from django.db import models
from django.urls import reverse


class Career(models.Model):
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('careers')

    def __str__(self):
        return self.id

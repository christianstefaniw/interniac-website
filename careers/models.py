from django.db import models
from django.urls import reverse
from django.utils import timezone

class Career(models.Model):
    content = models.TextField()
    posted = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def get_absolute_url(self):
        return reverse('careers')

    def __str__(self):
        return str(self.id)

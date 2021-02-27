import os

from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse
from django_unique_slugify import unique_slugify

from accounts.models import User

intern_types = (
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid')
)

intern_where = (
    ('Virtual', 'Virtual'),
    ('In-Person', 'In-Person')
)


class Listing(models.Model):
    company = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='listing')
    title = models.CharField(max_length=50)
    type = models.CharField(choices=intern_types, max_length=20)
    where = models.CharField(choices=intern_where, max_length=20)
    career = models.ForeignKey('Career', related_name='listings', blank=True, on_delete=models.CASCADE)
    new_career = models.CharField(blank=True, max_length=30)
    pay = models.CharField(blank=True, max_length=20)
    time_commitment = models.CharField(max_length=20)
    location = models.TextField(blank=True)
    application_deadline = models.DateTimeField()
    description = models.TextField()
    applications = models.ManyToManyField('accounts.User', related_name='applications', blank=True)
    acceptances = models.ManyToManyField('accounts.User', related_name='acceptances', blank=True)
    rejections = models.ManyToManyField('accounts.User', related_name='rejections', blank=True)
    saves = models.ManyToManyField('accounts.User', related_name='saves', blank=True)
    slug = models.SlugField(max_length=50, unique=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.title
        unique_slugify(self, self.slug)
        super(Listing, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listing', kwargs={'slug': self.slug})

    def accept_email(self, student):
        email = student.email

        message = f'''
Congratulations! You have been accepted to the {self.title} internship from {self.company}! 
If you have any questions for {self.company}, email them at {self.company.email} or reply to this message.
Good luck! 
                
From, the Interniac Team
                '''

        EmailMessage(body=message, from_email=os.environ.get("EMAIL"),
                     to=[email], subject=f"Congratulations! ({self.title})",
                     reply_to=[self.company.email]).send()

    def reject_email(self, student):
        email = student.email

        message = f'''
We are sorry to inform you that you have not been selected for the {self.title} internship from {self.company}.
If you have any questions for {self.company}, email them at {self.company.email} or reply to this message.
Better luck next time.

From, the Interniac Team
                    '''

        EmailMessage(body=message, from_email=os.environ.get("EMAIL"),
                     to=[email], subject=f"Response for {self.title}",
                     reply_to=[self.company.email]).send()

    def __str__(self):
        return self.title


class Career(models.Model):
    career = models.CharField(max_length=30)

    def __str__(self):
        return self.career

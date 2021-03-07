import os

import django
from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse
from django_unique_slugify import unique_slugify

from django.contrib.auth import get_user_model


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

    employer_acceptances = models.ManyToManyField('accounts.User', related_name='employer_acceptances')
    employer_rejections = models.ManyToManyField('accounts.User', related_name='employer_rejections')
    employer_interview_requests = models.ManyToManyField('accounts.User', related_name='employer_interview_requests')

    student_acceptances = models.ManyToManyField('accounts.User', related_name='student_acceptances')
    student_rejections = models.ManyToManyField('accounts.User', related_name='student_rejections')
    student_interview_requests = models.ManyToManyField('accounts.User', related_name='student_interview_requests')

    applications = models.ManyToManyField('accounts.User', related_name='applications', blank=True)
    acceptances = models.ManyToManyField('accounts.User', related_name='listing_acceptances', blank=True)
    rejections = models.ManyToManyField('accounts.User', related_name='listing_rejections', blank=True)
    interview_requests = models.ManyToManyField('accounts.User', related_name='interviews', blank=True)
    application_url = models.URLField(blank=True, null=True)
    posted = models.DateField(default=django.utils.timezone.now, blank=True)
    slug = models.SlugField(max_length=50, unique=False, blank=True)

    @property
    def summarize(self):
        data = {
            'company': self.company,
            'title': self.title,
            'where': self.where,
            'career': self.career,
            'pay': self.pay,
            'time_commitment': self.time_commitment,
            'location': self.location,
            'applications': [application for application in self.applications.all()],
            'rejections': [rejection for rejection in self.rejections.all()],
            'interview requests': [request for request in self.interview_requests.all()],
            'application url': self.application_url,
            'posted': self.posted,
            'slug': self.slug
        }

        return data

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

    def request_interview_email(self, student):
        email = student.email
        message = f'''
Congratulations, you have moved onto the next stage of the recruitment process for {self.company.employer_profile.company_name}.
{self.company.employer_profile.company_name} will schedule an interview with you shortly, if you have any questions please email 
{self.company.email} or reply to this email.

From, the Interniac Team
                            '''

        EmailMessage(body=message, from_email=os.environ.get("EMAIL"),
                     to=[email], subject=f"Next steps for {self.title}",
                     reply_to=[self.company.email]).send()

    def accept(self, user_id):
        user = get_user_model().objects.get(id=user_id)

        self.applications.remove(user)
        self.acceptances.add(user)
        self.employer_acceptances.add(user)
        self.student_acceptances.add(user)

        self.accept_email(user)

        if user in self.interview_requests.all():
            self.interview_requests.remove(user)

    def __str__(self):
        return self.title


class Career(models.Model):
    career = models.CharField(max_length=30)

    def __str__(self):
        return self.career

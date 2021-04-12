import os

from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from helpers.email import send_email_thread, send_email
from .helpers import *

INTERN_TYPES = (
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid')
)

INTERN_WHERE = (
    ('Virtual', 'Virtual'),
    ('In-Person', 'In-Person')
)


class Listing(models.Model):
    company = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='listing')
    title = models.CharField(max_length=50)
    type = models.CharField(choices=INTERN_TYPES, max_length=20)
    where = models.CharField(choices=INTERN_WHERE, max_length=20)
    career = models.ForeignKey(
        'Career', related_name='listings', blank=True, on_delete=models.CASCADE)
    new_career = models.CharField(blank=True, max_length=30)
    pay = models.CharField(blank=True, max_length=20)
    time_commitment = models.CharField(max_length=20)
    location = models.TextField(blank=True)
    application_deadline = models.DateTimeField()
    description = models.TextField()

    employer_acceptances = models.ManyToManyField(
        'accounts.User', related_name='employer_acceptances', blank=True)
    employer_rejections = models.ManyToManyField(
        'accounts.User', related_name='employer_rejections', blank=True)
    employer_interview_requests = models.ManyToManyField('accounts.User', related_name='employer_interview_requests',
                                                         blank=True)

    student_acceptances = models.ManyToManyField(
        'accounts.User', related_name='student_acceptances', blank=True)
    student_rejections = models.ManyToManyField(
        'accounts.User', related_name='student_rejections', blank=True)
    student_interview_requests = models.ManyToManyField('accounts.User', related_name='student_interview_requests',
                                                        blank=True)

    applications = models.ManyToManyField(
        'accounts.User', related_name='applications', blank=True)
    acceptances = models.ManyToManyField(
        'accounts.User', related_name='listing_acceptances', blank=True)
    rejections = models.ManyToManyField(
        'accounts.User', related_name='listing_rejections', blank=True)
    interview_requests = models.ManyToManyField(
        'accounts.User', related_name='interviews', blank=True)

    awaiting_confirm_acceptance = models.ManyToManyField(
        'accounts.User', related_name='awaiting_confirm_acceptance', blank=True
    )


    application_url = models.URLField(blank=True, null=True)
    posted = models.DateField(default=timezone.now, blank=True)
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

    def get_absolute_url(self):
        return reverse('listing', kwargs={'slug': self.slug})

    def applied_email(self, student_name):
        message = applied_msg(student_name, self.title)

        send_email_thread(body=message, from_email=os.environ.get("EMAIL"), to=[self.company.email],
                          subject=f"New Application ({self.title})",
                          reply_to=[os.environ.get("EMAIL")])

    def accept_email(self, student):
        email = student.email

        message = accept_msg(self.company, self.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[email], subject=f"Congratulations! ({self.title})",
                   reply_to=[self.company.email])

    def reject_email(self, student):
        email = student.email

        message = reject_msg(self.company, self.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[email], subject=f"Response for {self.title}",
                   reply_to=[self.company.email])

    def request_interview_email(self, student):
        email = student.email
        message = request_interview_msg(self.company)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[email], subject=f"Next steps for {self.title}",
                   reply_to=[self.company.email])

    def add_application(self, student):
        self.applications.add(student)

    def remove_application(self, student):
        self.applications.remove(student)

    def archive_student_acceptance(self, student):
        self.student_acceptances.remove(student)

    def archive_student_rejection(self, student):
        self.student_rejections.remove(student)

    def archive_interview_request(self, student):
        self.student_interview_requests.remove(student)

    def remove_from_interview(self, student):
        if student in self.interview_requests.all():
            self.interview_requests.remove(student)
        if student in self.student_interview_requests.all():
            self.student_interview_requests.remove(student)
        if student in self.employer_interview_requests.all():
            self.employer_interview_requests.remove(student)

    def decline_acceptance(self, student):
        self.awaiting_confirm_acceptance.remove(student)

        message = declined_message(f'{student.first_name} {student.last_name}', self.title)

        send_email(body=confirmed_message, from_email=os.environ.get("EMAIL"),
                   to=[self.company.email], subject=f"Student Declined",
                   reply_to=[student.email]
                   )

    def confirm_acceptance(self, student):
        for listing in student.applications.all():
            listing.remove_application(student)

        for listing in student.awaiting_confirm_acceptance.all():
            listing.awaiting_confirm_acceptance.remove(student)

        self.awaiting_confirm_acceptance.remove(student)
        self.acceptances.add(student)
        self.employer_acceptances.add(student)
        self.student_acceptances.add(student)

        message = confirmed_message(f'{student.first_name} {student.last_name}', self.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[self.company.email], subject=f"Student Confirmed!",
                   reply_to=[student.email]
                   )
        

    def accept(self, student):
        self.applications.remove(student)
        self.awaiting_confirm_acceptance.add(student)
        self.accept_email(student)
        self.remove_from_interview(student)

    def reject(self, student_id):
        user = get_user_model().objects.get(id=student_id)

        self.applications.remove(user)
        self.rejections.add(user)
        self.employer_rejections.add(user)
        self.student_rejections.add(user)

        self.reject_email(user)

        self.remove_from_interview(user.id)

    def request_interview(self, student_id):
        user = get_user_model().objects.get(id=student_id)

        self.interview_requests.add(user)
        self.employer_interview_requests.add(user)
        self.student_interview_requests.add(user)

        self.request_interview_email(user)

    def __str__(self):
        return self.title


class Career(models.Model):
    career = models.CharField(max_length=30)

    def __str__(self):
        return self.career

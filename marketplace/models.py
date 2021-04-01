import os

from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from helpers.email import send_email_thread, send_email


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

    employer_acceptances = models.ManyToManyField('accounts.User', related_name='employer_acceptances', blank=True)
    employer_rejections = models.ManyToManyField('accounts.User', related_name='employer_rejections', blank=True)
    employer_interview_requests = models.ManyToManyField('accounts.User', related_name='employer_interview_requests',
                                                         blank=True)

    student_acceptances = models.ManyToManyField('accounts.User', related_name='student_acceptances', blank=True)
    student_rejections = models.ManyToManyField('accounts.User', related_name='student_rejections', blank=True)
    student_interview_requests = models.ManyToManyField('accounts.User', related_name='student_interview_requests',
                                                        blank=True)

    applications = models.ManyToManyField('accounts.User', related_name='applications', blank=True)
    acceptances = models.ManyToManyField('accounts.User', related_name='listing_acceptances', blank=True)
    rejections = models.ManyToManyField('accounts.User', related_name='listing_rejections', blank=True)
    interview_requests = models.ManyToManyField('accounts.User', related_name='interviews', blank=True)

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
        message = f'''
        {student_name} has applied for {self.title}

        From, the Interniac Team
                        '''

        send_email_thread(body=message, from_email=os.environ.get("EMAIL"), to=[self.company.email],
                          subject=f"New Application ({self.title})",
                          reply_to=[os.environ.get("EMAIL")])

    def accept_email(self, student):
        email = student.email

        message = f'''
Congratulations! You have been accepted to the {self.title} internship from {self.company}! 
If you have any questions for {self.company}, email them at {self.company.email} or reply to this message.
Good luck! 

From, the Interniac Team
                '''

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                          to=[email], subject=f"Congratulations! ({self.title})",
                          reply_to=[self.company.email])

    def reject_email(self, student):
        email = student.email

        message = f'''
We are sorry to inform you that you have not been selected for the {self.title} internship from {self.company}.
If you have any questions for {self.company}, email them at {self.company.email} or reply to this message.
Better luck next time.

From, the Interniac Team
                    '''
        send_email(body=message, from_email=os.environ.get("EMAIL"),
                          to=[email], subject=f"Response for {self.title}",
                          reply_to=[self.company.email])

    def request_interview_email(self, student):
        email = student.email
        message = f'''
Congratulations, you have moved onto the next stage of the recruitment process for {self.company.employer_profile.company_name}.
{self.company.employer_profile.company_name} will schedule an interview with you shortly, if you have any questions please email 
{self.company.email} or reply to this email.

From, the Interniac Team
                            '''

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                          to=[email], subject=f"Next steps for {self.title}",
                          reply_to=[self.company.email])

    def remove_from_interview(self, student_id):
        user = get_user_model().objects.get(id=student_id)
        if user in self.interview_requests.all():
            self.interview_requests.remove(user)
        if user in self.student_interview_requests.all():
            self.student_interview_requests.remove(user)
        if user in self.employer_interview_requests.all():
            self.employer_interview_requests.remove(user)

    def accept(self, student_id):
        user = get_user_model().objects.get(id=student_id)

        self.applications.remove(user)
        self.acceptances.add(user)
        self.employer_acceptances.add(user)
        self.student_acceptances.add(user)

        self.accept_email(user)

        self.remove_from_interview(user.id)

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


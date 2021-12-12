from notifications.signals import notify

from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


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

    # students that have been accepted, rejected and requested
    # visible on the employer's account
    # needed in order to archive accepted/rejected student without affecting other accounts viewing the same field
    employer_acceptances = models.ManyToManyField(
        'accounts.User', related_name='employer_acceptances', blank=True)
    employer_rejections = models.ManyToManyField(
        'accounts.User', related_name='employer_rejections', blank=True)
    employer_interview_requests = models.ManyToManyField('accounts.User', related_name='employer_interview_requests',
                                                         blank=True)

    # students that have been accepted, rejected and requested
    # visible on the student's account
    # needed in order to archive the students acceptance/rejection/request without affecting other accounts viewing the same field
    student_acceptances = models.ManyToManyField(
        'accounts.User', related_name='student_acceptances', blank=True)
    student_rejections = models.ManyToManyField(
        'accounts.User', related_name='student_rejections', blank=True)
    student_interview_requests = models.ManyToManyField('accounts.User', related_name='student_interview_requests',
                                                        blank=True)

    # constant acceptances, rejections and requests
    # these are not viewed on any account
    # needed in order to create status updates
    acceptances = models.ManyToManyField(
        'accounts.User', related_name='listing_acceptances', blank=True)
    rejections = models.ManyToManyField(
        'accounts.User', related_name='listing_rejections', blank=True)
    interview_requests = models.ManyToManyField(
        'accounts.User', related_name='interviews', blank=True)

    # if all of the above was one group of fields, users would be affected by another users actions so
    # the state of a users application is kept in an isolated group

    awaiting_confirm_acceptance = models.ManyToManyField(
        'accounts.User', related_name='awaiting_confirm_acceptance', blank=True
    )
    applications = models.ManyToManyField(
        'accounts.User', related_name='applications', blank=True)

    application_url = models.URLField(blank=True, null=True)
    posted = models.DateField(default=timezone.now, blank=True)
    slug = models.SlugField(max_length=50, unique=False, blank=True)

    already_applied = models.ManyToManyField(
        'accounts.User', related_name='already_applied', blank=True)

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

    def has_student_already_applied(self, student) -> bool:
        return student in self.already_applied.all()

    def apply(self, student):
        self.add_application(student)
        if not self.has_student_already_applied(student):
            self.already_applied.add(student)

        if self.company.notifications.unread().filter(actor_object_id=self.id).filter(action_object_object_id=student.id).count() != 0:
            return

        notify.send(recipient=self.company, verb='someone applied!',
                    actor=self, sender=self, action_object=student)

    def unapply(self, student):
        self.remove_application(student)
        if student in self.interview_requests.all():
            self.interview_requests.remove(student)
        if student in self.student_interview_requests.all():
            self.student_interview_requests.remove(student)
        if student in self.employer_interview_requests.all():
            self.employer_interview_requests.remove(student)

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

    def check_if_accepted(self, user):
        return user in self.awaiting_confirm_acceptance.all()

    def remove_from_interview(self, student):
        if student in self.interview_requests.all():
            self.interview_requests.remove(student)
        if student in self.student_interview_requests.all():
            self.student_interview_requests.remove(student)
        if student in self.employer_interview_requests.all():
            self.employer_interview_requests.remove(student)

    def decline_acceptance(self, student):
        self.awaiting_confirm_acceptance.remove(student)

    def confirm_acceptance(self, student):
        for listing in student.applications.all():
            listing.remove_application(student)

        for listing in student.awaiting_confirm_acceptance.all():
            listing.awaiting_confirm_acceptance.remove(student)

        self.awaiting_confirm_acceptance.remove(student)
        self.acceptances.add(student)
        self.employer_acceptances.add(student)
        self.student_acceptances.add(student)

    def accept(self, student):
        self.applications.remove(student)
        self.awaiting_confirm_acceptance.add(student)
        self.remove_from_interview(student)

    def reject(self, student):

        self.applications.remove(student)
        self.rejections.add(student)
        self.employer_rejections.add(student)
        self.student_rejections.add(student)

        self.remove_from_interview(student)

    def request_interview(self, student):
        self.interview_requests.add(student)
        self.employer_interview_requests.add(student)
        self.student_interview_requests.add(student)

    def __str__(self):
        return self.title


class Career(models.Model):
    career = models.CharField(max_length=30)

    def __str__(self):
        return self.career

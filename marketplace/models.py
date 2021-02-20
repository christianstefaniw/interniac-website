from django.db import models


intern_types = (
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid')
)

intern_where = (
    ('Virtual', 'Virtual'),
    ('In-Person', 'In-Person')
)


class Listing(models.Model):
    org = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='listing')
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

    def __str__(self):
        return self.title


class Career(models.Model):
    career = models.CharField(max_length=30)

    def __str__(self):
        return self.career

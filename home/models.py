from django.db import models


class EmailSignup(models.Model):
    email_signup = models.EmailField()

    def __str__(self):
        return self.email_signup


class Statistics(models.Model):
    # There should only be one stats entry, same primary key will enforce this.
    # Throws integrity error if more than 1 entry
    enforce_one = models.TextField(default="Statistics", editable=False, primary_key=True)
    students = models.IntegerField()
    employers = models.IntegerField()
    professionals = models.IntegerField()

    def __str__(self):
        return "stats"


class Event(models.Model):
    datetime = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.TextField()
    meet_url = models.URLField()

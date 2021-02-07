from django.db import models


class EmailSignup(models.Model):
    email_signup = models.EmailField()

    def __str__(self):
        return self.email_signup


class Statistics(models.Model):
    students = models.IntegerField()
    employers = models.IntegerField()
    professionals = models.IntegerField()

    def __str__(self):
        return str(self.id)

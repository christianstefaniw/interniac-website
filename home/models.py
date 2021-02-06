from django.db import models


class EmailSignup(models.Model):
    email_signup = models.EmailField()

    def __str__(self):
        return self.email_signup

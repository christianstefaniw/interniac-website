import os

from django.core.mail import EmailMessage


def subscribe(form):
    email = form.cleaned_data['email_signup']
    EmailMessage(subject="Thank you!", body="Thank you for subscribing to Interniac's Mailing list!",
                 from_email=os.environ.get("EMAIL"), to=[email]).send()


def send_email(form):
    email = form.cleaned_data['email']
    name = form.cleaned_data['name']
    message = form.cleaned_data['message'] + f"\nFrom: {name}"
    EmailMessage(body=message, from_email=email, to=[os.environ.get("EMAIL")],
                 reply_to=[email]).send()

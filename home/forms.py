import os

from django import forms
from django.core.mail import EmailMessage
from nocaptcha_recaptcha import NoReCaptchaField

from .helpers import insert_into_spreadsheet


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    message = forms.CharField(widget=forms.Textarea())
    captcha = NoReCaptchaField(label='')

    def send_email(self):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        message = self.cleaned_data['message'] + f"\nFrom: {name}"
        EmailMessage(body=message, from_email=email, to=[os.environ.get("EMAIL")],
                     reply_to=[email]).send()


class EmailForm(forms.Form):
    email_signup = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    def is_valid(self):
        insert_into_spreadsheet(self.data['email_signup'])
        return super(EmailForm, self).is_valid()

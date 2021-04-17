import os

from django import forms
from nocaptcha_recaptcha import NoReCaptchaField

from helpers.email import send_email
from .helpers import insert_into_spreadsheet


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    message = forms.CharField(widget=forms.Textarea())
    captcha = NoReCaptchaField(label='', required=False)

    def send_email(self):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        message = self.cleaned_data['message'] + f"\nFrom: {name}"
        send_email(body=message, from_email=email, to=[os.environ.get("EMAIL")],
                          reply_to=[email], subject=f'Message from {name}')


class EmailForm(forms.Form):
    email_signup = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    def is_valid(self):
        insert_into_spreadsheet(self.data['email_signup'])
        send_email(from_email=os.environ.get('EMAIL'), body='Thank you for signing up for our newsletter.',
                          to=[self.data['email_signup']], reply_to=[None], subject='Thank you!')
        return super(EmailForm, self).is_valid()

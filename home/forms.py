import os

from django import forms
from django.core.mail import EmailMessage
from nocaptcha_recaptcha import NoReCaptchaField

from .models import EmailSignup


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class': 'msg-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'msg-input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'msg-text-area'}))
    captcha = NoReCaptchaField(label='')

    def send_email(self):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        message = self.cleaned_data['message'] + f"\nFrom: {name}"
        EmailMessage(body=message, from_email=email, to=[os.environ.get("EMAIL")],
                     reply_to=[email]).send()


class EmailForm(forms.ModelForm):
    email_signup = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'id': 'signup-newsletter'}))

    class Meta:
        model = EmailSignup
        fields = ['email_signup']

    def subscribed_email(self):
        email = self.cleaned_data['email_signup']
        EmailMessage(subject="Thank you!", body="Thank you for subscribing to Interniac's Mailing list!",
                     from_email=os.environ.get("EMAIL"), to=[email]).send()

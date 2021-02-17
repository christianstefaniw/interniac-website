from django import forms
from nocaptcha_recaptcha import NoReCaptchaField

from .models import EmailSignup


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class': 'msg-input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'msg-input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'msg-text-area'}))
    captcha = NoReCaptchaField(label='')


class EmailForm(forms.ModelForm):
    email_signup = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'id': 'signup-newsletter'}))

    class Meta:
        model = EmailSignup
        fields = ['email_signup']

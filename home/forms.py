from django import forms

from .models import EmailSignup


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())


class EmailForm(forms.ModelForm):
    email_signup = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    class Meta:
        model = EmailSignup
        fields = ['email_signup']

from django import forms
from django.forms import DateInput
from nocaptcha_recaptcha import NoReCaptchaField

from accounts.models import User, EmployerProfile
from .models import Listing, Career


class Filter(forms.Form):
    FILTERS_TYPE = [
        ('paid', 'paid'),
        ('unpaid', 'unpaid')
    ]
    FILTERS_WHERE = [
        ('virtual', 'virtual'),
        ('in-person', 'in-person')
    ]
    WHERE_AND_EMPTY = [('', 'all')] + FILTERS_WHERE
    TYPES_AND_EMPTY = [('', 'all')] + FILTERS_TYPE

    type = forms.ChoiceField(choices=TYPES_AND_EMPTY, widget=forms.CheckboxSelectMultiple)
    where = forms.ChoiceField(choices=WHERE_AND_EMPTY, widget=forms.CheckboxSelectMultiple)
    career = forms.ModelChoiceField(queryset=Career.objects.all(), widget=forms.CheckboxSelectMultiple)
    company = forms.ModelChoiceField(queryset=EmployerProfile.objects.all(), widget=forms.CheckboxSelectMultiple)


class CreateListingForm(forms.ModelForm):
    new_career = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Create a new career'}), required=False)
    captcha = NoReCaptchaField(label='')

    class Meta:
        model = Listing
        widgets = {
            'application_deadline': DateInput(attrs={'type': 'date'})
        }
        exclude = ['company', 'applications']

from django import forms
from nocaptcha_recaptcha import NoReCaptchaField

from accounts.models import EmployerProfile
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
    WHERE_AND_EMPTY = [('', '---------')] + FILTERS_WHERE
    TYPES_AND_EMPTY = [('', '---------')] + FILTERS_TYPE

    type = forms.ChoiceField(choices=TYPES_AND_EMPTY,
                             )
    where = forms.ChoiceField(choices=WHERE_AND_EMPTY,
                              )
    career = forms.ModelChoiceField(
        queryset=Career.objects.all(), )
    company = forms.ModelChoiceField(
        queryset=EmployerProfile.objects.all())


class CreateListingForm(forms.ModelForm):
    new_career = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Create a new career'}), required=False)
    application_url = forms.URLField(widget=forms.URLInput(
        attrs={'placeholder': 'optional'}), required=False)
    captcha = NoReCaptchaField(label='', required=False)

    class Meta:
        model = Listing
        widgets = {
            'application_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format="%d %b %Y %H:%M %Z")
        }
        fields = ('title', 'type', 'pay', 'where', 'location', 'career', 'new_career',
                  'time_commitment', 'application_deadline', 'description', 'application_url')

    def clean(self):
        cleaned_data = super(CreateListingForm, self).clean()

        if cleaned_data['where'] == 'Virtual':
            if cleaned_data['location'] != '' and cleaned_data['location'] is not None:
                cleaned_data['location'] = ''

        if cleaned_data['where'] == 'In-Person':
            if cleaned_data['location'] == '' or cleaned_data['location'] is None:
                self.add_error('location', 'Must have a location')

        if cleaned_data['type'] == 'Paid':
            if cleaned_data['pay'] == '' or cleaned_data['pay'] is None:
                self.add_error('pay', 'Paid internship must have a salary')

        if cleaned_data['type'] == 'Unpaid':
            if cleaned_data['pay'] != '' and cleaned_data['pay'] is not None:
                cleaned_data['pay'] = ''

        if cleaned_data['career'] is not None and cleaned_data['career'] != '':
            if cleaned_data['new_career'] != '' and cleaned_data['new_career'] is not None:
                cleaned_data['new_career'] = ''

        if cleaned_data['career'] is None or cleaned_data['career'] == '':
            if cleaned_data['new_career'] == '' or cleaned_data['new_career'] is None:
                self.add_error('career', 'Please select a career')

        return cleaned_data

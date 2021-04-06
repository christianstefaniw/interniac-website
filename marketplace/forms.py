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
    WHERE_AND_EMPTY = [('', 'all')] + FILTERS_WHERE
    TYPES_AND_EMPTY = [('', 'all')] + FILTERS_TYPE

    type = forms.ChoiceField(choices=TYPES_AND_EMPTY, widget=forms.CheckboxSelectMultiple)
    where = forms.ChoiceField(choices=WHERE_AND_EMPTY, widget=forms.CheckboxSelectMultiple)
    career = forms.ModelChoiceField(queryset=Career.objects.all(), widget=forms.CheckboxSelectMultiple)
    company = forms.ModelChoiceField(queryset=EmployerProfile.objects.all(), widget=forms.CheckboxSelectMultiple)


class CreateListingForm(forms.ModelForm):
    new_career = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Create a new career'}), required=False)
    application_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'optional'}), required=False)
    captcha = NoReCaptchaField(label='')

    class Meta:
        model = Listing
        widgets = {
            'application_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format="%d %b %Y %H:%M %Z")
        }
        exclude = ['company']

    def clean(self):
        cleaned_data = super(CreateListingForm, self).clean()
        if cleaned_data['where'] == 'Virtual':
            if cleaned_data['location'] is not '' and cleaned_data['location'] is not None:
                self.add_error('where', 'Virtual internship can\'t have a location')

        if cleaned_data['where'] == 'in-person':
            if cleaned_data['where'] is '' or cleaned_data['where'] is None:
                self.add_error('where', 'Must have a location')

        if cleaned_data['type'] == 'Unpaid':
            if cleaned_data['pay'] is not '' and cleaned_data['pay'] is not None:
                self.add_error('type', 'Unpaid internship can\'t have a salary')

        if cleaned_data['career'] is not None and cleaned_data['career'] is not '':
            if cleaned_data['new_career'] is not '' and cleaned_data['new_career'] is not None:
                self.add_error('career', 'Can\'t make a new career if there is a selected career')

        return cleaned_data

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
    captcha = NoReCaptchaField(label='', required=False)

    class Meta:
        model = Listing
        widgets = {
            'application_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format="%d %b %Y %H:%M %Z")
        }
        exclude = ['company']

    def clean(self):
        cleaned_data = super(CreateListingForm, self).clean()

        if cleaned_data['where'] == 'Virtual':
            if cleaned_data['location'] != '' and cleaned_data['location'] != None:
                self.add_error('where', 'Virtual internship can\'t have a location')

        if cleaned_data['where'] == 'In-Person':
            if cleaned_data['location'] == '' or cleaned_data['location'] == None:
                self.add_error('where', 'Must have a location')

        if cleaned_data['type'] == 'Paid':
            if cleaned_data['pay'] == '' or cleaned_data['pay'] == None:
                self.add_error('pay', 'Paid internship must have a salary')

        if cleaned_data['type'] == 'Unpaid':
            if cleaned_data['pay'] != '' and cleaned_data['pay'] != None:
                self.add_error('type', 'Unpaid internship can\'t have a salary')

        if cleaned_data['career'] != None and cleaned_data['career'] != '':
            if cleaned_data['new_career'] != '' and cleaned_data['new_career'] != None:
                self.add_error('career', 'Can\'t make a new career if there is a selected career')

        return cleaned_data

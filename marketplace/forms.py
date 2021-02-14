from django import forms

from .models import Listing, Career

FILTERS_TYPE = [
    ('paid', 'paid'),
    ('unpaid', 'unpaid')
]

TYPES_AND_EMPTY = [('', 'all')] + FILTERS_TYPE

FILTERS_WHERE = [
    ('virtual', 'virtual'),
    ('in-person', 'in-person')
]

WHERE_AND_EMPTY = [('', 'all')] + FILTERS_WHERE


class Filter(forms.Form):
    type = forms.ChoiceField(choices=TYPES_AND_EMPTY)
    where = forms.ChoiceField(choices=WHERE_AND_EMPTY)
    career = forms.ModelChoiceField(queryset=Career.objects.all(), empty_label='all')


class CreateListingForm(forms.ModelForm):
    new_career = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Create a new career'}), required=False)

    class Meta:
        model = Listing
        exclude = ['org']

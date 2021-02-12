from django import forms
from .models import Listing, Career


class CreateListingForm(forms.ModelForm):
    new_career = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Create a new career'}), required=False)

    class Meta:
        model = Listing
        exclude = ['org']

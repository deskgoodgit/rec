from django import forms
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    candidate_id = forms.CharField(
        max_length=7, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Candidate ID here'
        })
    )

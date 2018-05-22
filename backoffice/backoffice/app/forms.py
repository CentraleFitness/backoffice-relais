"""
Definition of forms.
"""
import re
from django import forms
from .models import apiKey
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class apiKeyForm(forms.ModelForm):

    class Meta:
        model = apiKey
        fields = ('api_key',)


class GymForm(forms.Form):
    name = forms.CharField()
    desc = forms.CharField(required=False)
    address = forms.CharField()
    alt_address = forms.CharField(required=False)
    zip = forms.CharField(max_length=5, min_length=5)
    city = forms.CharField()
    phone = forms.CharField(max_length=10, min_length=10)
    email = forms.EmailField()

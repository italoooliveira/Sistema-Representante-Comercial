from ..models import *
from django import forms
from django.forms import ModelForm

class ConfiguracoesForm(forms.Form):
    pe01 = forms.BooleanField(required=False)
    pe02 = forms.CharField(max_length=100)


from ..models import *
from django import forms
from django.forms import ModelForm


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'
        widgets = {
            'senha': forms.PasswordInput(render_value=True)
        }


class PesquisaUsuarioForm(forms.Form):
    nome = forms.CharField(required=False, max_length=255)
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


class UsuarioFormCustom(forms.Form):
    PERMISSOES = (
        ('BASICA', 'BÁSICA'),
        ('PREPOSTO', 'PREPOSTO'),
        ('ADMINISTRADOR', 'ADMINISTRADOR'),
    )

    email = forms.CharField()
    senha = forms.CharField(max_length=200, required=False, widget=forms.PasswordInput)
    permissao = forms.ChoiceField(choices=PERMISSOES)
    nome = forms.CharField(max_length=255)
    telefone = forms.CharField(max_length=80, required=False)
    widgets = {
        'senha': forms.PasswordInput(render_value=False)
    }


class PesquisaUsuarioForm(forms.Form):
    nome = forms.CharField(required=False, max_length=255)
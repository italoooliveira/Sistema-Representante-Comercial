from ..models import *
from django import forms
from django_select2 import forms as s2forms

class CustomizacoesForm(forms.Form):
    chamada = forms.CharField(max_length=100)
    descricao = forms.CharField(max_length=255)
    empresa = forms.ModelChoiceField(queryset=Empresas.objects.none())
    produtos = forms.ModelMultipleChoiceField(queryset=Produtos.objects.none(), widget=s2forms.Select2MultipleWidget())

    def __init__(self, *args, **kwargs):
        super(CustomizacoesForm, self).__init__(*args, **kwargs)
        #self.fields['produtos'].queryset = Produtos.objects.none()
        self.fields['empresa'].queryset = Empresas.objects.all()

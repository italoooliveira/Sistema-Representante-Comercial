from ..models import *
from django import forms
from django.forms import ModelForm


class TipoEmpresaForm(ModelForm):
    class Meta:
        model = TiposEmpresa
        labels: {'Tipo'}
        fields = '__all__'


class PesquisaTipoEmpresaForm(forms.Form):
    tipo = forms.CharField(required=False, max_length=255)


class MinhaEmpresaForm(ModelForm):
    class Meta:
        model = MinhaEmpresa
        fields = '__all__'


class EmpresaForm(ModelForm):
    class Meta:
        model = Empresas
        fields = '__all__'


class PesquisaEmpresaForm(forms.Form):
    razao_social = forms.CharField(max_length=255, required=False)
    nome_fantasia = forms.CharField(max_length=255, required=False)
    cnpj = forms.CharField(max_length=50, required=False)
    inscricao_estadual = forms.CharField(max_length=25, required=False)
    tipo_empresa = forms.ModelChoiceField(required=False, queryset=TiposEmpresa.objects.none())

    def __init__(self, *args, **kwargs):
        super(PesquisaEmpresaForm, self).__init__(*args, **kwargs)
        self.fields['tipo_empresa'].queryset = TiposEmpresa.objects.all()


class ClienteForm(ModelForm):
    class Meta:
        model = Clientes
        fields = '__all__'


class PesquisaClienteForm(forms.Form):
    razao_social = forms.CharField(max_length=255, required=False)
    nome_fantasia = forms.CharField(max_length=255, required=False)
    cnpj = forms.CharField(max_length=50, required=False)
    inscricao_estadual = forms.CharField(max_length=25, required=False)


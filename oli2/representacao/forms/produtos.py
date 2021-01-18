from ..models import *
from django import forms
from django.forms import ModelForm
from django_select2 import forms as s2forms


class CategoriaForm(ModelForm):
    class Meta:
        model = Categorias
        fields = '__all__'


class PesquisaCategoriaForm(forms.Form):
    nome_categoria = forms.CharField(required=False, max_length=255)


class UnidadeVendaForm(ModelForm):
    class Meta:
        model = UnidadesVenda
        fields = '__all__'


class PesquisaUnidadeVendaForm(forms.Form):
    sigla = forms.CharField(required=False, max_length=255)


class TipoEmbalagemForm(ModelForm):
    class Meta:
        model = TiposEmbalagem
        fields = '__all__'


class PesquisaTipoEmbalagemForm(forms.Form):
    tipo = forms.CharField(required=False, max_length=255)


class ProdutoForm(ModelForm):
    class Meta:
        model = Produtos
        fields = '__all__'
        widgets = {
            'empresa': s2forms.Select2MultipleWidget()
        }


class PesquisaProdutoForm(forms.Form):
    descricao = forms.CharField(required=False, max_length=255)
    codigo_produto = forms.CharField(required=False, max_length=150)
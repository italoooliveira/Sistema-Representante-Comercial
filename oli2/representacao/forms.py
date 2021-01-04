from .models import *
from django import forms
from django.forms import ModelForm
from tempus_dominus.widgets import DatePicker, TimePicker
from django_select2 import forms as s2forms


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'
        widgets = {
            'senha': forms.PasswordInput(render_value=True)
        }


class PesquisaUsuarioForm(forms.Form):
    nome = forms.CharField(required=False, max_length=255)


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


class PrepostoForm(ModelForm):
    class Meta:
        model = Prepostos
        fields = '__all__'
        widgets = {
            'id_usuario': forms.HiddenInput(),
            'empresa': s2forms.Select2MultipleWidget(),
            'cliente': s2forms.Select2MultipleWidget(),
        }


class PesquisaPrepostoForm(forms.Form):
    nome = forms.CharField(required=False, max_length=255)


class RotaPrepostoForm(forms.Form):
    pass


class ContatoForm(ModelForm):
    class Meta:
        model = Contatos
        fields = '__all__'
        widgets = {
            'empresa': s2forms.Select2MultipleWidget(),
            'cliente': s2forms.Select2MultipleWidget(),
        }


class PesquisaContatoForm(forms.Form):
    nome_contato = forms.CharField(required=False, max_length=255)


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


class FormaPagamentoForm(ModelForm):
    class Meta:
        model = FormasPagamento
        fields = '__all__'


class PesquisaFormaPagamentoForm(forms.Form):
    nome_forma_pagamento = forms.CharField(required=False, max_length=80)
    prazo = forms.CharField(required=False, max_length=200)


class PedidoForm(ModelForm):
    class Meta:
        model = Pedidos
        fields = '__all__'
        widgets = {
            'data_pedido': DatePicker(
                options={
                    "useCurrent": True,
                }
            ),
            'data_entrega': DatePicker(),
            'horario_pedido': forms.TimeInput(
                format='%H:%M'
            )
        }


class PesquisaPedidoForm(forms.Form):
    numero_pedido = forms.IntegerField(required=False)
    data_inicial_pedido = forms.DateField(required=False,widget=DatePicker())
    data_final_pedido = forms.DateField(required=False,widget=DatePicker())
    empresa_representada = forms.ModelChoiceField(required=False, queryset=Empresas.objects.none())
    empresa_cliente = forms.ModelChoiceField(required=False, queryset=Clientes.objects.none())
    usuario_responsavel = forms.ModelChoiceField(required=False, queryset=Usuarios.objects.none())

    def __init__(self, *args, **kwargs):
        super(PesquisaPedidoForm, self).__init__(*args, **kwargs)
        self.fields['empresa_representada'].queryset = Empresas.objects.all()
        self.fields['empresa_cliente'].queryset = Clientes.objects.all()
        self.fields['usuario_responsavel'].queryset = Usuarios.objects.all()


class AcompanhamentoForm(ModelForm):
    class Meta:
        model = Acompanhamentos
        fields = '__all__'
        widgets = {
            'data_inicial': DatePicker(),
            'data_final': DatePicker(),
        }


class ProspeccoesClientesForm(forms.Form):
    QUANTIDADE = (
        ('TODOS', 'TODOS OS USUÁRIOS'),
        ('1', 'USUÁRIO QUE MAIS PROSPECTOU'),
        ('5', '5 USUÁRIOS QUE MAIS PROSPECTARAM'),
        ('15', '15 USUÁRIOS QUE MAIS PROSPECTARAM'),
        ('30', '30 USUÁRIOS QUE MAIS PROSPECTARAM'),
        ('50', '50 USUÁRIOS QUE MAIS PROSPECTARAM')
    )

    TIPO_PESQUISA = (
        ('Filtrar Todos', 'Filtrar todos'),
        ('Filtrar especifico', 'Filtrar específico')
    )

    usuario = forms.ModelChoiceField(required=False, queryset=Usuarios.objects.none())
    quantidade_maxima = forms.ChoiceField(required=False, choices=QUANTIDADE)
    tipo_pesquisa = forms.ChoiceField(required=False, choices=TIPO_PESQUISA, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(ProspeccoesClientesForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuarios.objects.all()


class ClientesSemPedidoForm(forms.Form):
    data_inicial = forms.DateField(required=True, widget=DatePicker())
    data_final = forms.DateField(required=True, widget=DatePicker())


class CancelamentoPedidosPorCliente(forms.Form):
    data_inicial = forms.DateField(required=False, widget=DatePicker())
    data_final = forms.DateField(required=False, widget=DatePicker())
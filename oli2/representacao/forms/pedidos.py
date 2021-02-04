from ..models import *
from django import forms
from django.forms import ModelForm
from tempus_dominus.widgets import DatePicker


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
    STATUS = (
        ('', '---------'),
        ('AGUARDANDO FATURAMENTO', 'AGUARDANDO FATURAMENTO'),
        ('FATURADO', 'FATURADO'),
        ('CANCELADO', 'CANCELADO')
    )

    numero_pedido = forms.IntegerField(required=False)
    data_inicial_pedido = forms.DateField(required=False,widget=DatePicker())
    data_final_pedido = forms.DateField(required=False,widget=DatePicker())
    empresa_representada = forms.ModelChoiceField(required=False, queryset=Empresas.objects.none())
    empresa_cliente = forms.ModelChoiceField(required=False, queryset=Clientes.objects.none())
    usuario_responsavel = forms.ModelChoiceField(required=False, queryset=Usuarios.objects.none())
    status_pedido = forms.ChoiceField(required=False, choices=STATUS)

    def __init__(self, *args, **kwargs):
        super(PesquisaPedidoForm, self).__init__(*args, **kwargs)
        self.fields['empresa_representada'].queryset = Empresas.objects.all()
        self.fields['empresa_cliente'].queryset = Clientes.objects.all()
        self.fields['usuario_responsavel'].queryset = Usuarios.objects.all()
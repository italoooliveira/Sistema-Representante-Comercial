from ..models import *
from django import forms
from django.forms import ModelForm
from tempus_dominus.widgets import DatePicker


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
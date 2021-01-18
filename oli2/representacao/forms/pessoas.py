from ..models import *
from django import forms
from django.forms import ModelForm
from django_select2 import forms as s2forms


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
    FREQUENCIA = (
        ('SEMANAL', 'SEMANAL'),
        ('QUINZENAL', 'QUINZENAL'),
        ('MENSAL', 'MENSAL'),
        ('OUTRA', 'OUTRA')
    )

    nome_rota = forms.CharField(required=False, max_length=255)
    prepostos = forms.ModelChoiceField(required=False, queryset=Prepostos.objects.none())
    clientes = forms.ModelChoiceField(required=False, queryset=Clientes.objects.none())
    frequencia = forms.ChoiceField(choices=FREQUENCIA)

    def __init__(self, *args, **kwargs):
        super(RotaPrepostoForm, self).__init__(*args, **kwargs)
        self.fields['prepostos'].queryset = Prepostos.objects.all()
        self.fields['clientes'].queryset = Clientes.objects.all()


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
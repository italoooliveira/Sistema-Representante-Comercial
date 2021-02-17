from ..models import *
from django import forms
from django.forms import ModelForm
from django_select2 import forms as s2forms
from tempus_dominus.widgets import DatePicker


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


class PesquisaUsuarioForm(forms.Form):
    nome = forms.CharField(required=False, max_length=255)


class TarefaForm(ModelForm):
    class Meta:
        model = Tarefas
        fields = '__all__'
        widgets = {
            'data_inicial': DatePicker(
                options={
                    "useCurrent": True,
                }
            ),
            'data_final': DatePicker(),
            'usuario': s2forms.Select2MultipleWidget(),
        }


class PesquisaTarefaForm(forms.Form):
    STATUS = (
        ('', '------'),
        ('A FAZER', 'A FAZER'),
        ('EM ANDAMENTO', 'EM ANDAMENTO'),
        ('CONCLUIDA', 'CONCLUÍDA'),
        ('REVISAO', 'REVISÃO'),
        ('CANCELADA', 'CANCELADA')
    )

    descricao_tarefa = forms.CharField(required=False, max_length=800)
    data_inicial = forms.DateField(required=False, widget=DatePicker())
    data_final = forms.DateField(required=False, widget=DatePicker())
    status = forms.ChoiceField(required=False, choices=STATUS)
    minhas_tarefas = forms.BooleanField(required=False)


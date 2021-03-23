import distutils
from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .funcoes import *

@login_required
def configuracoes_pedidos(request, template_name='configuracoes/configuracoes_pedidos.html'):
    pe01 = get_object_or_404(Configuracoes, pk=1)
    pe02 = get_object_or_404(Configuracoes, pk=2)

    if request.method == "POST":
        form = ConfiguracoesForm(request.POST)
        if form.is_valid():
            pe01.valor = form.cleaned_data['pe01']
            pe01.save()
            pe02.valor = form.cleaned_data['pe02']
            pe02.save()

    else:
        form = ConfiguracoesForm()
        form.fields['pe01'].initial = eval(pe01.valor)
        form.fields['pe02'].initial = pe02.valor

    return render(request, template_name, {'form': form, 'pe01': pe01, 'pe02': pe02})
import json
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from ..forms import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .funcoes import *

@login_required
def criar_oferta(request, template_name='customizacoes/ofertas_form.html'):
    form = CustomizacoesForm(request.POST or None)

    if request.method == 'POST':

        template_name = 'customizacoes/oferta_imprimir.html'
        chamada = request.POST['chamada']
        descricao = request.POST['descricao']
        produtos = request.POST['produtos']

        logoMinhaEmpresa = get_object_or_404(MinhaEmpresa, pk=1).logo
        logo = get_object_or_404(Empresas, pk=request.POST['empresa']).logo

        return render(request, template_name, {'chamada': chamada, 'descricao': descricao, 'produtos': produtos, 'logoMinhaEmpresa': logoMinhaEmpresa, 'logo': logo})

    produtos = Produtos.objects.all()
    return render(request, template_name, {'form': form, 'produtos': produtos})

@csrf_exempt
def retorna_informacoes_produtos_empresa(request):
    if request.is_ajax() and request.method == "POST":
        data = request.body
        id_empresa = json.loads(data)
        empresa = get_object_or_404(Empresas, pk=id_empresa)
        produtos = Produtos.objects.filter(empresa=empresa).all().values()
        print(produtos)

        return JsonResponse({'produtos_empresa': list(produtos)})

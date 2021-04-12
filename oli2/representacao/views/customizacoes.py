import json
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def criar_oferta(request, template_name='customizacoes/ofertas_form.html'):
    form = CustomizacoesForm(request.POST or None)

    if form.is_valid():
        chamada = form.cleaned_data['chamada']
        descricao = form.cleaned_data['descricao']
        logo_empresa = form.cleaned_data['empresa'].logo.url
        produtos = form.cleaned_data['produtos']

        request.session['logo_empresa'] = logo_empresa
        request.session['chamada'] = chamada
        request.session['descricao'] = descricao
        request.session['produtos'] = list(produtos.values('id_produto'))

        return redirect('gerar-imagem-oferta')
    produtos = Produtos.objects.all()

    return render(request, template_name, {'form': form, 'produtos': produtos})


@csrf_exempt
def retorna_informacoes_produtos_empresa(request):
    if request.is_ajax() and request.method == "POST":
        data = request.body
        id_empresa = json.loads(data)
        empresa = get_object_or_404(Empresas, pk=id_empresa)
        produtos = Produtos.objects.filter(empresa=empresa).all().values()

        return JsonResponse({'produtos_empresa': list(produtos)})


@csrf_exempt
def gerar_imagem(request, template_name='customizacoes/gerador_imagem.html'):
    logo_empresa = request.session.get('logo_empresa')
    chamada = request.session.get('chamada')
    descricao = request.session.get('descricao')
    produtos_ids = request.session.get('produtos')
    ids = []

    for produto_id in produtos_ids:
        ids.append(produto_id['id_produto'])

    produtos_banco = Produtos.objects.filter(id_produto__in=ids).all()
    minha_empresa = get_object_or_404(MinhaEmpresa, pk=1)
    logo_minha_empresa = minha_empresa.logo.url

    return render(request, template_name, {'logo_empresa': logo_empresa, 'logo_minha_empresa':logo_minha_empresa, 'produtos': produtos_banco, 'descricao': descricao, 'chamada':chamada})


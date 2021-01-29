from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .funcoes import *
import json


# Empresas #
# Tipos de Empresa #


@login_required
def listar_tipos_empresa(request, template_name='empresas/lista_tipos_empresa.html'):
    form = PesquisaTipoEmpresaForm(request.GET or None)

    listaTiposEmpresa = TiposEmpresa.objects.order_by('tipo').all()

    if 'tipo' in request.GET:
        tipo = request.GET['tipo']

        if tipo:
            listaTiposEmpresa = TiposEmpresa.objects.order_by('tipo').filter(Q(tipo__icontains=tipo)).all()

    paginator = Paginator(listaTiposEmpresa, 15)
    page = request.GET.get('page')
    tipos_empresa_por_pagina = paginator.get_page(page)
    data = {'tipos_empresa': tipos_empresa_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_tipo_empresa(request, template_name='empresas/tipo_empresa_form.html'):
    form = TipoEmpresaForm(request.POST or None)

    if form.is_valid():
        form.save()

        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-tipo-empresa')
    return render(request, template_name, {'form': form})


@login_required
def editar_tipo_empresa(request, id_tipo_empresa, template_name='empresas/tipo_empresa_form.html'):
    tipoEmpresa = get_object_or_404(TiposEmpresa, pk=id_tipo_empresa)

    if request.method == "POST":
        form = TipoEmpresaForm(request.POST, instance=tipoEmpresa)
        if form.is_valid():
            form.save()
            return redirect('tipos-empresa')
    else:
        form = TipoEmpresaForm(instance=tipoEmpresa)
    return render(request, template_name, {'form': form})


@login_required
def excluir_tipo_empresa(request, id_tipo_empresa):
    tipoEmpresa = get_object_or_404(TiposEmpresa, pk=id_tipo_empresa)

    if request.method == "GET":
        tipoEmpresa.delete()
        return redirect('tipos-empresa')


# Tipos de Empresa #

# Minha empresa #


@login_required
def cadastrar_minha_empresa(request, template_name='empresas/minha_empresa_form.html'):
    minha_empresa = MinhaEmpresa.objects.first()

    if minha_empresa:
        return redirect('editar-minha-empresa', minha_empresa.id_minha_empresa)
    else:
        form = MinhaEmpresaForm(request.POST or None)

        if request.method == "POST":
            form = MinhaEmpresaForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()

                mensagem_cadastro_sucesso(request)

                return redirect('cadastrar-minha-empresa')
        return render(request, template_name, {'form': form})


@login_required
def editar_minha_empresa(request, id_minha_empresa, template_name='empresas/minha_empresa_form.html'):
    minha_empresa = get_object_or_404(MinhaEmpresa, pk=id_minha_empresa)

    if request.method == "POST":
        form = MinhaEmpresaForm(request.POST, request.FILES, instance=minha_empresa)

        if form.is_valid():
            form.save()

            mensagem_edicao_sucesso(request)

            return redirect('cadastrar-minha-empresa')
    else:
        form = MinhaEmpresaForm(instance=minha_empresa)
    return render(request, template_name, {'form': form})


# Minha empresa #

# Empresa #


@login_required
def listar_empresas(request, template_name='empresas/lista_empresas.html'):
    form = PesquisaEmpresaForm(request.GET or None)

    listaEmpresa = Empresas.objects.order_by('nome_fantasia')

    if 'razao_social' in request.GET:
        razao_social = request.GET['razao_social']

        if razao_social:
            listaEmpresa = listaEmpresa.filter(Q(razao_social__icontains=razao_social))

    if 'nome_fantasia' in request.GET:
        nome_fantasia = request.GET['nome_fantasia']

        if nome_fantasia:
            listaEmpresa = listaEmpresa.filter(Q(nome_fantasia__icontains=nome_fantasia))

    if 'cnpj' in request.GET:
        cnpj = request.GET['cnpj']

        if cnpj:
            listaEmpresa = listaEmpresa.filter(cnpj=cnpj)

    if 'inscricao_estadual' in request.GET:
        inscricao_estadual = request.GET['inscricao_estadual']

        if inscricao_estadual:
            listaEmpresa = listaEmpresa.filter(inscricao_estadual=inscricao_estadual)

    if 'tipo_empresa' in request.GET:
        tipo_empresa = request.GET['tipo_empresa']

        if tipo_empresa:
            tipo=get_object_or_404(Empresas, pk=tipo_empresa)
            listaEmpresa = listaEmpresa.filter(id_tipo_empresa=tipo)

    listaEmpresa = listaEmpresa.all().values(
        'id_empresa',
        'nome_fantasia',
        'razao_social',
        'cnpj',
        'inscricao_estadual',
        'telefone',
        'email',
        'logo'
    )

    paginator = Paginator(listaEmpresa, 15)
    page = request.GET.get('page')
    empresas_por_pagina = paginator.get_page(page)

    data = {'empresas': empresas_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_empresa(request, template_name='empresas/empresa_form.html'):
    form = EmpresaForm(request.POST or None)

    if request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            mensagem_cadastro_sucesso(request)

            return redirect('cadastrar-empresa')
    return render(request, template_name, {'form': form})


@login_required
def editar_empresa(request, id_empresa, template_name='empresas/empresa_form.html'):
    empresa = get_object_or_404(Empresas, pk=id_empresa)

    if request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)

        if form.is_valid():
            form.save()
            return redirect('empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, template_name, {'form': form})


@login_required
def excluir_empresa(request, id_empresa):
    empresa = get_object_or_404(Empresas, pk=id_empresa)

    if request.method == "GET":
        empresa.delete()
        return redirect('empresas')


# Empresa #


# Cliente #


@login_required
def listar_clientes(request, template_name='empresas/lista_clientes.html'):
    form = PesquisaClienteForm(request.GET or None)

    listaCliente = Clientes.objects.order_by('nome_fantasia')

    if 'razao_social' in request.GET:
        razao_social = request.GET['razao_social']

        if razao_social:
            listaCliente = listaCliente.filter(Q(razao_social__icontains=razao_social))

    if 'nome_fantasia' in request.GET:
        fantasia = request.GET['fantasia']

        if fantasia:
            listaCliente = listaCliente.filter(Q(nome_fantasia__icontains=fantasia))

    if 'cnpj' in request.GET:
        cnpj = request.GET['cnpj']

        if cnpj:
            listaCliente = listaCliente.filter(cnpj=cnpj)

    if 'inscricao_estadual' in request.GET:
        inscricao_estadual = request.GET['inscricao_estadual']

        if inscricao_estadual:
            listaCliente = listaCliente.filter(inscricao_estadual=inscricao_estadual)

    listaCliente = listaCliente.all().values(
        'id_cliente',
        'nome_fantasia',
        'razao_social',
        'cnpj',
        'inscricao_estadual',
        'telefone',
        'email',
        'logo'
    )
    paginator = Paginator(listaCliente, 15)
    page = request.GET.get('page')
    clientes_por_pagina = paginator.get_page(page)

    data = {'clientes': clientes_por_pagina, 'form': form}

    return render(request, template_name, data)

@csrf_exempt
def buscar_dados_clientes(request):
    if request.is_ajax() and request.method == "POST":
        data = request.body
        id_cliente = json.loads(data)

        cliente = get_object_or_404(Clientes, pk=id_cliente)
        cliente_serializado = serializers.serialize('json', [ cliente ])

        return HttpResponse(cliente_serializado, content_type="text/json-comment-filtered")


@login_required
def cadastrar_cliente(request, template_name='empresas/cliente_form.html'):
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()

        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-cliente')
    return render(request, template_name, {'form': form})


@login_required
def editar_cliente(request, id_cliente, template_name='empresas/cliente_form.html'):
    cliente = get_object_or_404(Clientes, pk=id_cliente)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cadastrar-clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, template_name, {'form': form})


@login_required
def excluir_cliente(request, id_cliente):
    cliente = get_object_or_404(Clientes, pk=id_cliente)

    if request.method == "GET":
        cliente.delete()
        return redirect('clientes')


# Cliente #
# Empresas #
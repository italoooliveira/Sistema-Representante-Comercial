from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from io import StringIO, BytesIO
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .functions import render_pdf_view
import json
import base64
import pandas as pd
import matplotlib.pyplot as plt


def login(request, template_name='usuarios/login.html'):
    return render(request, template_name)


def autenticar(request):
    email = request.POST['email']
    senha = request.POST['senha']
    proxima = request.POST['next']

    if User.objects.filter(email=email).exists():
        username = User.objects.filter(email=email).values_list('username', flat=True).get()
        user = auth.authenticate(request, username=username, password=senha)

        if user is not None:
            auth.login(request, user)

            if proxima:
                return redirect(proxima)
            else:
                return redirect('index')
    return render(request, 'usuarios/login.html')


def logout(request, template_name='usuarios/login.html'):
    auth.logout(request, template_name)


def mensagem_edicao_sucesso(request):
    messages.success(request, 'Atualizado com sucesso')


def mensagem_cadastro_sucesso(request):
    messages.success(request, 'Cadastro realizado com sucesso')


@login_required
def index(request, template_name='index.html'):
    return render(request, template_name)


# Usuários #


@login_required
def listar_usuarios(request, template_name='usuarios/lista_usuarios.html'):
    form = PesquisaUsuarioForm(request.GET or None)

    listaUsuario = Usuarios.objects.order_by('nome')

    if 'nome' in request.GET:
        nome = request.GET['nome']

        if nome:
            listaUsuario = listaUsuario.filter(Q(nome__icontains=nome))

    listaUsuario = listaUsuario.all().values('id_usuario', 'nome', 'email', 'telefone')
    paginator = Paginator(listaUsuario, 15)
    page = request.GET.get('page')
    usuarios_por_pagina = paginator.get_page(page)

    data = {'usuarios': usuarios_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_usuario(request, template_name='usuarios/usuario_form.html'):
    form = UsuarioForm(request.POST or None)

    if request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']
        permissao = request.POST['permissao']
        nome = request.POST['nome']
        telefone = request.POST['telefone']

        user = User.objects.create_user(username=nome, email=email)
        user.set_password(senha)
        user.save()

        senha_bytes = senha.encode('ascii')
        senha_base64_bytes = base64.b64encode(senha_bytes)
        senha_base64_bytes = senha_base64_bytes.decode("ascii")
        usuario = Usuarios(nome=nome, email=email, senha=senha_base64_bytes, permissao=permissao, telefone=telefone, django_auth_user=user)
        usuario.save()

        mensagem_cadastro_sucesso(request)

        if permissao == "PREPOSTO":
            preposto = Prepostos(id_usuario=usuario.id)
            preposto.save()

        return redirect('cadastrar-usuario')
    return render(request, template_name, {'form': form})


@login_required
def editar_usuario(request, id_usuario, template_name='usuarios/usuario_form.html'):
    usuario = get_object_or_404(Usuarios, pk=id_usuario)
    base64_string = usuario.senha
    base64_bytes = base64_string.encode("ascii")
    senha_string_bytes = base64.b64decode(base64_bytes)
    senha_string = senha_string_bytes.decode("ascii")
    usuario.senha = senha_string

    if request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']
        permissao = request.POST['permissao']
        nome = request.POST['nome']
        telefone = request.POST['telefone']

        usuario.email = email
        permissao_original = usuario.permissao
        usuario.permissao = permissao
        senha_bytes = senha.encode('ascii')
        senha_base64_bytes = base64.b64encode(senha_bytes)
        senha_base64_bytes = senha_base64_bytes.decode("ascii")
        usuario.senha = senha_base64_bytes
        usuario.nome = nome
        usuario.telefone = telefone
        usuario.save()

        user = get_object_or_404(User, pk=usuario.django_auth_user.id)
        user.username = nome
        user.email = email
        user.set_password(senha)
        user.save()

        if permissao != permissao_original and permissao == "PREPOSTO":
            preposto = Prepostos(id_usuario=usuario.id)
            preposto.save()

        return redirect('usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, template_name, {'form': form})


@login_required
def excluir_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuarios, pk=id_usuario)

    if request.method == "GET":
        usuario.delete()

        user = get_object_or_404(User, pk=usuario.django_auth_user.id)
        user.delete()

        return redirect('usuarios')

# Usuários #


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


# Pessoas #
# Preposto #


@login_required
def listar_prepostos(request, template_name='pessoas/lista_prepostos.html'):
    form = PesquisaPrepostoForm(request.GET or None)

    listaPrepostos = Prepostos.objects.select_related('id_usuario').all()

    if 'nome' in request.GET:
        nome = request.GET['nome'];

        if nome:
            listaPrepostos = Prepostos.objects.filter(id_usuario__nome__icontains=nome).all()

    listaPrepostosModificada = []

    for preposto in listaPrepostos:
        listaPrepostosModificada.append(
            {
                 'id_preposto': preposto.id_preposto,
                 'comissao': preposto.comissao,
                 'possui_vinculo_empresa': preposto.possui_vinculo_empresa,
                 'nome': preposto.id_usuario.nome,
                 'email': preposto.id_usuario.email,
                 'telefone': preposto.id_usuario.telefone
            }
        )

    paginator = Paginator(listaPrepostosModificada, 15)
    page = request.GET.get('page')
    prepostos_por_pagina = paginator.get_page(page)

    data = {'prepostos': prepostos_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_preposto(request, template_name='pessoas/preposto_form.html'):
    form = PrepostoForm(request.POST or None)

    if form.is_valid():
        new = form.save(commit=False)
        new.save()
        form.save_m2m()

        return redirect('cadastrar-preposto')
    return render(request, template_name, {'form': form})


@login_required
def editar_preposto(request, id_preposto, template_name='pessoas/preposto_form.html'):
    prepostoUsuario = Prepostos.objects.select_related('id_usuario').get(id_preposto=id_preposto)
    preposto = get_object_or_404(Prepostos, pk=id_preposto)

    if request.method == "POST":
        form = PrepostoForm(request.POST, instance=preposto)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
            return redirect('prepostos')
    else:
        form = PrepostoForm(instance=preposto)
    return render(request, template_name, {'form': form, 'preposto': prepostoUsuario})


@login_required
def excluir_preposto(request, id_preposto):
    preposto = get_object_or_404(Prepostos, pk=id_preposto)

    if request.method == "GET":
        preposto.delete()
        return redirect('prepostos')


def cadastrar_rotas_prepostos(request, template_name='pessoas/rotas_prepostos_form.html'):
    form = RotaPrepostoForm(request.POST or None)
    prepostos = Prepostos.objects.filter().select_related('id_usuario').all()

    return render(request, template_name, {'form':form, 'prepostos': prepostos})


# Preposto #


# Contato #


@login_required
def listar_contatos(request, template_name='pessoas/lista_contatos.html'):
    form = PesquisaContatoForm(request.GET or None)

    listaContatos = Contatos.objects.order_by('nome_contato')

    if 'nome_contato' in request.GET:
        nome_contato = request.GET['nome_contato'];

        if nome_contato:
            listaContatos = listaContatos.filter(Q(nome_contato__icontains=nome_contato))

    listaContatos = listaContatos.all().values('id_contato', 'nome_contato', 'email', 'telefone', 'cargo')
    paginator = Paginator(listaContatos, 15)
    page = request.GET.get('page')
    contatos_por_pagina = paginator.get_page(page)

    data = {'contatos': contatos_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_contato(request, template_name='pessoas/contato_form.html'):
    form = ContatoForm(request.POST or None)

    if form.is_valid():
        new = form.save(commit=False)
        new.save()
        form.save_m2m()

        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-contato')
    return render(request, template_name, {'form': form})


@login_required
def editar_contato(request, id_contato, template_name='pessoas/contato_form.html'):
    contato = get_object_or_404(Contatos, pk=id_contato)

    if request.method == "POST":
        form = PrepostoForm(request.POST, instance=contato)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
            return redirect('contatos')
    else:
        form = ContatoForm(instance=contato)
    return render(request, template_name, {'form': form})


@login_required
def excluir_contato(request, id_contato):
    contato = get_object_or_404(Contatos, pk=id_contato)

    if request.method == "GET":
        contato.delete()
        return redirect('contatos')


# Contato #
# Pessoas #


# Produtos #
# Categoria #


@login_required
def listar_categorias(request, template_name='produtos/lista_categorias.html'):
    form = PesquisaCategoriaForm(request.GET or None)

    listaCategorias = Categorias.objects.order_by('nome_categoria')

    if 'nome_categoria' in request.GET:
        nome_categoria = request.GET['nome_categoria']

        if nome_categoria:
            listaCategorias = listaCategorias.filter(Q(nome_categoria__icontains=nome_categoria))

    listaCategorias = listaCategorias.all()
    paginator = Paginator(listaCategorias, 15)
    page = request.GET.get('page')
    categorias_por_pagina = paginator.get_page(page)

    data = {'categorias': categorias_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_categoria(request, template_name='produtos/categoria_form.html'):
    form = CategoriaForm(request.POST or None)

    if form.is_valid():
        form.save()

        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-categoria')
    return render(request, template_name, {'form': form})


@login_required
def editar_categoria(request, id_categoria, template_name='produtos/categoria_form.html'):
    categoria = get_object_or_404(Categorias, pk=id_categoria)

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, template_name, {'form': form})


@login_required
def excluir_categoria(request, id_categoria):
    categoria = get_object_or_404(Categorias, pk=id_categoria)

    if request.method == "GET":
        categoria.delete()
        return redirect('categorias')


# Categoria #


# Unidade Venda #


@login_required
def listar_unidades_venda(request, template_name='produtos/lista_unidades_venda.html'):
    form = PesquisaUnidadeVendaForm(request.GET or None)

    listaUnidadesVenda = UnidadesVenda.objects.order_by('sigla').all()

    if 'sigla' in request.GET:
        sigla = request.GET['sigla']

        if sigla:
            listaUnidadesVenda = UnidadesVenda.objects.order_by('sigla').filter(Q(sigla__icontains=sigla)).all()

    paginator = Paginator(listaUnidadesVenda, 15)
    page = request.GET.get('page')
    unidades_venda_por_pagina = paginator.get_page(page)

    data = {'unidades_venda': unidades_venda_por_pagina, 'form':form}

    return render(request, template_name, data)


@login_required
def cadastrar_unidade_venda(request, template_name='produtos/unidade_venda_form.html'):
    form = UnidadeVendaForm(request.POST or None)

    if form.is_valid():
        form.save()

        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-unidade-venda')
    return render(request, template_name, {'form': form})


@login_required
def editar_unidade_venda(request, id_unidade_venda, template_name='produtos/unidade_venda_form.html'):
    unidadeVenda = get_object_or_404(UnidadesVenda, pk=id_unidade_venda)

    if request.method == "POST":
        form = UnidadeVendaForm(request.POST, instance=unidadeVenda)

        if form.is_valid():
            form.save()
            return redirect('unidades-venda')
    else:
        form = UnidadeVendaForm(instance=unidadeVenda)
    return render(request, template_name, {'form': form})


@login_required
def excluir_unidade_venda(request, id_unidade_venda):
    unidadeVenda = UnidadesVenda.objects.get(pk=id_unidade_venda)

    if request.method == "GET":
        unidadeVenda.delete()
        return redirect('unidades-venda')


# Unidade Venda #


# Tipo Embalagem #


@login_required
def listar_tipos_embalagem(request, template_name='produtos/lista_tipos_embalagem.html'):
    form = PesquisaTipoEmbalagemForm(request.GET or None)

    listaTiposEmbalagem = TiposEmbalagem.objects.order_by('tipo').all()

    if 'tipo' in request.GET:
        tipo = request.GET['tipo']

        if tipo:
            listaTiposEmbalagem = TiposEmbalagem.objects.order_by('tipo').filter(Q(tipo__icontains=tipo)).all()

    paginator = Paginator(listaTiposEmbalagem, 15)
    page = request.GET.get('page')
    tipos_embalagem_por_pagina = paginator.get_page(page)

    data = {'tipos_embalagem': tipos_embalagem_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_tipo_embalagem(request, template_name='produtos/tipo_embalagem_form.html'):
    form = TipoEmbalagemForm(request.POST or None)

    if form.is_valid():
        form.save()

        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-tipo-embalagem')
    return render(request, template_name, {'form': form})


@login_required
def editar_tipo_embalagem(request, id_tipo_embalagem, template_name='produtos/tipo_embalagem_form.html'):
    tipoEmbalagem = get_object_or_404(TiposEmbalagem, pk=id_tipo_embalagem)

    if request.method == "POST":
        form = TipoEmbalagemForm(request.POST, instance=tipoEmbalagem)
        if form.is_valid():
            form.save()
            return redirect('tipos-embalagem')
    else:
        form = TipoEmbalagemForm(instance=tipoEmbalagem)
    return render(request, template_name, {'form': form})


@login_required
def excluir_tipo_embalagem(request, id_tipo_embalagem):
    tipoEmbalagem = get_object_or_404(TiposEmbalagem, pk=id_tipo_embalagem)

    if request.method == "GET":
        tipoEmbalagem.delete()
        return redirect('tipos-embalagem')


# Tipo Embalagem #


# Produto #

@login_required
def listar_produtos(request, template_name='produtos/lista_produtos.html'):
    form = PesquisaProdutoForm(request.GET or None)

    listaProduto = Produtos.objects.order_by('descricao')

    if 'descricao' in request.GET:
        descricao = request.GET['descricao']

        if descricao:
            listaProduto = listaProduto.filter(Q(descricao__icontains=descricao))

    if 'codigo_produto' in request.GET:
        codigo_produto = request.GET['codigo_produto']

        if codigo_produto:
            listaProduto = listaProduto.filter(Q(codigo_produto__icontains=codigo_produto))

    listaProduto = listaProduto.all().values(
        'id_produto',
        'descricao',
        'codigo_produto',
        'custo_unitario',
        'imagem'
    )
    paginator = Paginator(listaProduto, 15)
    page = request.GET.get('page')
    produtos_por_pagina = paginator.get_page(page)

    data = {'produtos': produtos_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_produto(request, template_name='produtos/produto_form.html'):
    form = ProdutoForm(request.POST or None)

    if form.is_valid():
        form = ProdutoForm(request.POST, request.FILES)
        new = form.save(commit=False)
        new.save()
        form.save_m2m()

        mensagem_cadastro_sucesso(request)

        return redirect('produtos')
    return render(request, template_name, {'form': form})


@login_required
def editar_produto(request, id_produto, template_name='produtos/produto_form.html'):
    produto = get_object_or_404(Produtos, pk=id_produto)

    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES, instance=produto)

        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
            return redirect('produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, template_name, {'form': form})


@login_required
def excluir_produto(request, id_produto):
    produto = get_object_or_404(Produtos, pk=id_produto)

    if request.method == "GET":
        produto.delete()
        return redirect('produtos')


# Produto #
# Produtos #


# Pedidos #
# Forma de pagamento #


@login_required
def listar_formas_pagamento(request, template_name='pedidos/lista_formas_pagamento.html'):
    form = PesquisaFormaPagamentoForm(request.GET or None)

    listaFormasPagamento = FormasPagamento.objects.order_by('nome_forma_pagamento')

    if 'nome_forma_pagamento' in request.GET:
        nome_forma_pagamento = request.GET['nome_forma_pagamento']

        if nome_forma_pagamento:
            listaFormasPagamento = listaFormasPagamento.filter(Q(nome_forma_pagamento__icontains=nome_forma_pagamento))

    if 'prazo' in request.GET:
        prazo = request.GET['prazo']

        if prazo:
            listaFormasPagamento = listaFormasPagamento.filter(prazo=prazo)

    listaFormasPagamento = listaFormasPagamento.all()
    paginator = Paginator(listaFormasPagamento, 15)
    page = request.GET.get('page')
    formas_pagamento_por_pagina = paginator.get_page(page)

    data = {'formas_pagamento': formas_pagamento_por_pagina, 'form':form}

    return render(request, template_name, data)


@login_required
def cadastrar_forma_pagamento(request, template_name='pedidos/forma_pagamento_form.html'):
    form = FormaPagamentoForm(request.POST or None)

    if form.is_valid():
        form.save()

        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-forma-pagamento')
    return render(request, template_name, {'form': form})


@login_required
def editar_forma_pagamento(request, id_forma_pagamento, template_name='pedidos/forma_pagamento_form.html'):
    formaPagamento = get_object_or_404(FormasPagamento, pk=id_forma_pagamento)

    if request.method == "POST":
        form = FormaPagamentoForm(request.POST, instance=formaPagamento)
        if form.is_valid():
            form.save()
            return redirect('formas-pagamento')
    else:
        form = FormaPagamentoForm(instance=formaPagamento)
    return render(request, template_name, {'form': form})


@login_required
def excluir_forma_pagamento(request, id_forma_pagamento):
    formaPagamento = FormasPagamento.objects.get(pk=id_forma_pagamento)

    if request.method == "POST":
        formaPagamento.delete()
        return redirect('formas-pagamento')


# Forma de pagamento #

# Pedido #


@login_required
def listar_pedidos(request, template_name='pedidos/lista_pedidos.html'):
    form = PesquisaPedidoForm(request.GET or None)

    listaPedido = Pedidos.objects.order_by('-data_pedido')

    if 'numero_pedido' in request.GET:
        numero_pedido = request.GET['numero_pedido']

        if numero_pedido:
            listaPedido = listaPedido.filter(numero_pedido=numero_pedido)

    if 'data_inicial_pedido' in request.GET:
        data_inicial_pedido = request.GET['data_inicial_pedido']

        if data_inicial_pedido:
            data_inicial_pedido = datetime.strptime(data_inicial_pedido, '%d/%m/%Y').strftime('%Y-%m-%d')
            listaPedido = listaPedido.filter(data_pedido__gte=data_inicial_pedido)

    if 'data_final_pedido' in request.GET:
        data_final_pedido = request.GET['data_final_pedido']

        if data_final_pedido:
            data_final_pedido = datetime.strptime(data_final_pedido, '%d/%m/%Y').strftime('%Y-%m-%d')
            listaPedido = listaPedido.filter(data_pedido__lte=data_final_pedido)

    if 'empresa_representada' in request.GET:
        empresa_representada = request.GET['empresa_representada']

        if empresa_representada:
            empresa=get_object_or_404(Empresas, pk=empresa_representada)
            listaPedido = listaPedido.filter(id_empresa_representada=empresa)

    if 'empresa_cliente' in request.GET:
        empresa_cliente = request.GET['empresa_cliente']

        if empresa_cliente:
            cliente = get_object_or_404(Clientes, pk=empresa_cliente)
            listaPedido = listaPedido.filter(id_empresa_cliente=cliente)

    if 'usuario_responsavel' in request.GET:
        usuario_responsavel = request.GET['usuario_responsavel']

        if usuario_responsavel:
            usuario = get_object_or_404(Usuarios, pk=usuario_responsavel)
            listaPedido = listaPedido.filter(id_usuario=usuario)

    listaPedido = listaPedido.select_related('id_empresa_representada','id_empresa_cliente').all()
    paginator = Paginator(listaPedido, 15)
    page = request.GET.get('page')
    pedidos_por_pagina = paginator.get_page(page)

    data = {'pedidos': pedidos_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_pedido(request, template_name='pedidos/pedido_form.html'):
    form = PedidoForm(request.POST or None)

    '''
    if request.method == "POST":
        id_usuario = request.POST['id_usuario']
        numero_pedido = request.POST['numero_pedido']
        id_empresa_representada = request.POST['id_empresa_representada']
        id_empresa_cliente = request.POST['id_empresa_cliente']
        data_pedido = request.POST['data_pedido']
        data_entrega = request.POST['data_entrega']
        id_forma_pagamento = request.POST['id_forma_pagamento']
        id_contato = request.POST['id_contato']
        observacao = request.POST['observacao']
        ordem_compra = request.POST['ordem_compra']

        pedido = Pedidos(
            id_usuario=get_object_or_404(Usuarios, pk=id_usuario),
            numero_pedido=numero_pedido,
            id_empresa_representada=get_object_or_404(Empresas, pk=id_empresa_representada),
            id_empresa_cliente=get_object_or_404(Clientes, pk=id_empresa_cliente),
            data_pedido=datetime.strptime(data_pedido, '%d/%m/%Y').strftime('%Y-%m-%d'),
            data_entrega=datetime.strptime(data_entrega, '%d/%m/%Y').strftime('%Y-%m-%d'),
            id_forma_pagamento=get_object_or_404(FormasPagamento, pk=id_forma_pagamento),
            id_contato=get_object_or_404(Contatos, pk=id_contato),
            observacao=observacao,
            ordem_compra=ordem_compra
        )

        pedido.save()
    '''

    if form.is_valid():
        pedido = form.save()

        mensagem_cadastro_sucesso(request)

        return redirect('confirmar-itens-pedido', pedido.pk)
    return render(request, template_name, {'form': form})


@login_required
def confirmar_itens_pedido(request, id_pedido, template_name='pedidos/confirmar_itens_pedido.html'):
    return render(request, template_name, {'id_pedido':id_pedido})


@login_required
def editar_pedido(request, id_pedido, template_name='pedidos/pedido_form.html'):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)

    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()

            return redirect('pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, template_name, {'form': form, 'id': id_pedido})


@login_required
@csrf_exempt
def cadastrar_itens_pedido(request, id_pedido, template_name='pedidos/itens_pedido_form.html'):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    representada = get_object_or_404(Empresas, pk=pedido.id_empresa_representada.id_empresa)
    produtos = Produtos.objects.filter(empresa=representada).all()

    if request.is_ajax() and request.method == "POST":
        data = request.body
        items = json.loads(data)

        total_pedido = 0

        for item in items:
            item_json = json.loads(item)

            total_pedido = total_pedido + item_json['custo_total']

            item_pedido = ItensPedido(
                id_pedido=pedido,
                id_produto=get_object_or_404(Produtos, pk=item_json['id_produto']),
                quantidade=item_json['quantidade'],
                custo_total=item_json['custo_total']
            )

            item_pedido.save()

            pedido.total_pedido = total_pedido
            pedido.save()

            mensagem_cadastro_sucesso(request)
        return HttpResponse("<p>Ok</p>")
    else:
        return render(request, template_name, {'id':pedido.id_pedido, 'pedido': pedido, 'representada': representada, 'produtos': produtos})


@login_required
@csrf_exempt
def editar_itens_pedido(request, id_pedido, template_name='pedidos/itens_pedido_form.html'):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    representada = get_object_or_404(Empresas, pk=pedido.id_empresa_representada.id_empresa)
    produtos = Produtos.objects.filter(empresa=representada).all()
    itens_pedido = ItensPedido.objects.filter(id_pedido=pedido).select_related("id_produto").all()

    if request.is_ajax() and request.method == "POST":
        data = request.body
        items = json.loads(data)

        ItensPedido.objects.filter(id_pedido=pedido).delete()

        total_pedido = 0

        for item in items:
            item_json = json.loads(item)

            total_pedido = total_pedido + item_json['custo_total']

            item_pedido = ItensPedido(
                id_pedido=pedido,
                id_produto=get_object_or_404(Produtos, pk=item_json['id_produto']),
                quantidade=item_json['quantidade'],
                custo_total=item_json['custo_total']
            )

            item_pedido.save()

            pedido.total_pedido = total_pedido
            pedido.save()
        return HttpResponse("<p>Ok</p>")
    else:
        return render(request, template_name, {'id': pedido.id_pedido, 'pedido': pedido, 'itens': itens_pedido, 'representada': representada, 'produtos':produtos})


@login_required
def excluir_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)

    if request.method == "GET":
        pedido.delete()

        return redirect('pedidos')


@login_required
def gerar_pdf_pedido(request, id_pedido, template_name='pedidos/pdf_pedido.html'):
    minha_empresa = MinhaEmpresa.objects.first()
    pedido = Pedidos.objects.select_related("id_empresa_representada", "id_empresa_cliente", "id_forma_pagamento").get(id_pedido=id_pedido)
    itens_pedido = ItensPedido.objects.filter(id_pedido=pedido).select_related("id_produto").all()

    pdf = render_pdf_view(request, template_name, {
        'pedido': pedido,
        'itens': itens_pedido,
        'minha_empresa': minha_empresa,
        'base_url': request.META['HTTP_HOST']
    })

    return HttpResponse(pdf, content_type='application/pdf')

# Pedido #
# Pedidos #


# Relatórios #

@login_required
def acompanhamentos(request, template_name='relatorios/lista_acompanhamentos.html'):
    listaAcompanhamento = Acompanhamentos.objects.all().values()

    paginator = Paginator(listaAcompanhamento, 15)
    page = request.GET.get('page')
    acompanhamentos_por_pagina = paginator.get_page(page)

    data = {'acompanhamentos': acompanhamentos_por_pagina}

    return render(request, template_name, data)


@login_required
def cadastrar_acompanhamento(request, template_name='relatorios/acompanhamento_form.html'):
    form = AcompanhamentoForm(request.POST or None)

    if request.method == "POST":
        mensagem_cadastro_sucesso(request)

        return redirect('cadastrar-acompanhamento')
    return render(request, template_name, {
        'form': form,
        'total_faturado_ate': 0.00,
        'percentual_da_meta_ate': 0.00,
        'tendencia_de_faturamento': 0.00,
        'faturamento_diario_necessario': 0.00,
        'tendencia': 0.00,
        'porcentagem': 0.00
    })


@login_required
def editar_acompanhamento(request, id_acompanhamento ,template_name='relatorios/acompanhamento_form.html'):
    acompanhamento = get_object_or_404(Acompanhamentos, pk=id_acompanhamento)
    listaPedidos = Pedidos.objects.filter(data_pedido__range=(acompanhamento.data_inicial, acompanhamento.data_final)).all().values()

    df = pd.DataFrame(listaPedidos)

    total_faturado_ate = df['total_pedido'].sum()
    percentual_da_meta_ate = total_faturado_ate / (acompanhamento.meta_geral / 100)
    tendencia_de_faturamento = (total_faturado_ate / acompanhamento.dias_trabalhados) * acompanhamento.dias_uteis
    faturamento_diario_necessario = (acompanhamento.meta_geral - total_faturado_ate) / (acompanhamento.dias_uteis - acompanhamento.dias_trabalhados)

    fig = plt.figure(figsize=(8, 4))
    plt.bar(['Total faturado até o momento(R$)','Tendência de faturamento final(R$)','Meta Geral(R$)'], [total_faturado_ate, tendencia_de_faturamento, acompanhamento.meta_geral], width=0.2, color=['green','red', 'blue'], align='center')
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    tendencia = base64.b64encode(image_png)
    tendencia = tendencia.decode('utf-8')

    fig2 = plt.figure(figsize=(8, 4))
    plt.bar(['Total faturado até o momento(%)','Tendência de faturamento final(%)','Meta Geral(%)'], [percentual_da_meta_ate, (tendencia_de_faturamento/(acompanhamento.meta_geral/100)), 100], width=0.2, color=['green','red', 'blue'], align='center')
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    porcentagem = base64.b64encode(image_png)
    porcentagem = porcentagem.decode('utf-8')

    if request.method == "POST":
        form = AcompanhamentoForm(request.POST, instance=acompanhamento)

        if form.is_valid():
            form.save()

            mensagem_edicao_sucesso(request)

            return redirect('editar-acompanhamento', id_acompanhamento)
    else:
        form = AcompanhamentoForm(instance=acompanhamento)

    return render(
        request,
        template_name,
        {
            'form': form,
            'meta_geral': acompanhamento.meta_geral,
            'total_faturado_ate': total_faturado_ate,
            'percentual_da_meta_ate': percentual_da_meta_ate,
            'tendencia_de_faturamento': tendencia_de_faturamento,
            'faturamento_diario_necessario': faturamento_diario_necessario,
            'tendencia': tendencia,
            'porcentagem': porcentagem
       }
    )


@login_required
def excluir_acompanhamento(request, id_acompanhamento):
    acompanhamento = get_object_or_404(Acompanhamentos, pk=id_acompanhamento)

    if request.method == "GET":
        acompanhamento.delete()
        return redirect('acompanhamentos')


@login_required
def prospeccoes_clientes(request, template_name='relatorios/prospeccao_clientes_form.html'):
    form = ProspeccoesClientesForm(request.GET or None)

    return render(request, template_name, {'form': form})


@login_required
def clientes_sem_pedido(request, template_name='relatorios/clientes_sem_pedido_form.html'):
    form = ClientesSemPedidoForm(request.GET or None)

    listaClientes = Clientes.objects.all().values()
    listaPedidos = Pedidos.objects.all().values()

    clientes_sem_pedidos = []

    if 'data_inicial' in request.GET and 'data_final' in request.GET:
        data_inicial = request.GET['data_inicial']
        data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y').strftime('%Y-%m-%d')
        data_final = request.GET['data_final']
        data_final = datetime.strptime(data_final, '%d/%m/%Y').strftime('%Y-%m-%d')

        dfClientes = pd.DataFrame(listaClientes)
        dfPedidos = pd.DataFrame(listaPedidos)
        dfPedidos['data_pedido'] = pd.to_datetime(dfPedidos['data_pedido'])

        dfPedidosIntervalo = dfPedidos.loc[(dfPedidos.data_pedido >= data_inicial) & (dfPedidos.data_pedido <= data_final)]
        dfPedidosDataAnteriorInicial = dfPedidos.loc[dfPedidos.data_pedido < data_inicial]
        dfClientesSemPedido = dfClientes[~dfClientes['id_cliente'].isin(dfPedidosIntervalo['id_empresa_cliente_id'])]
        dfClientesSemPedidoComUltimoPedido = retorna_ultimo_pedido(dfClientesSemPedido, dfPedidosDataAnteriorInicial)

        clientes_sem_pedido_list = dfClientesSemPedidoComUltimoPedido.values.tolist()

        for item in clientes_sem_pedido_list:
            if item[1] != "":
                clientes_sem_pedido.append({'nome_fantasia': item[1],'data_ultimo_pedido': item[-1]})
            else:
                clientes_sem_pedidos.append({'nome_fantasia': item[2],'data_ultimo_pedido': item[-1]})
    return render(request, template_name, {'form': form, 'clientes_sem_pedidos': clientes_sem_pedidos})


def retorna_ultimo_pedido(dfClientesSemPedido, dfPedidos):
    for index, row in dfClientesSemPedido.iterrows():
        if not dfPedidos.empty:
            dfUltimoPedido = dfPedidos.loc[dfPedidos.id_empresa_cliente_id == row.id_cliente].tail(1)
            dfClientesSemPedido['ultimo_pedido'] = dfUltimoPedido.iloc[0]['data_pedido']
        else:
            dfClientesSemPedido['ultimo_pedido'] = ''
    return dfClientesSemPedido


def cancelamento_pedidos_por_cliente(request, template_name='relatorios/cancelamento_pedidos_por_cliente_form.html'):
    form = CancelamentoPedidosPorCliente(request.GET or None)

    clientes_pedidos_somas = []

    if 'data_inicial' in request.GET and 'data_final' in request.GET:
        data_inicial = request.GET['data_inicial']
        data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y').strftime('%Y-%m-%d')
        data_final = request.GET['data_final']
        data_final = datetime.strptime(data_final, '%d/%m/%Y').strftime('%Y-%m-%d')

        listaClientes = Clientes.objects.all().values()
        listaPedidos = Pedidos.objects.filter(data_pedido__range=(data_inicial, data_final)).all().values()

        dfClientes = pd.DataFrame(listaClientes)
        dfPedidos = pd.DataFrame(listaPedidos)

        dfPedidosNaoCancelados = dfPedidos.loc[dfPedidos.status != "CANCELADO"]
        dfPedidosCancelados = dfPedidos.loc[dfPedidos.status == "CANCELADO"]

        dfClientesPedidosSomas = dfClientes[dfClientes['id_cliente'].isin(dfPedidos['id_empresa_cliente_id'])]
        dfClientesPedidosSomas = retorna_resultado(dfClientesPedidosSomas, dfPedidosNaoCancelados, dfPedidosCancelados)

        clientes_pedidos_somas_list = dfClientesPedidosSomas.values.tolist()

        for item in clientes_pedidos_somas_list:
            if (item[1] != ""):
                clientes_pedidos_somas.append(
                    {
                        'nome_fantasia': item[1],
                        'pedidos_feitos': int(item[-1]),
                        'pedidos_cancelados': int(item[-2]),
                        'pedidos_nao_cancelados': int(item[-3]),
                    }
                )
            else:
                clientes_pedidos_somas.append(
                    {
                        'nome_fantasia': item[2],
                        'pedidos_feitos': int(item[-1]),
                        'pedidos_cancelados': int(item[-2]),
                        'pedidos_nao_cancelados': int(item[-3]),
                    }
                )

    return render(request, template_name, {'form': form, 'clientes_pedidos_somas':clientes_pedidos_somas})


def retorna_resultado(dfClientesPedidosSomas, dfPedidosNaoCancelados, dfPedidosCancelados):
    for index, row in dfClientesPedidosSomas.iterrows():
        dfSomaPedidosNaoCancelados = 0
        dfSomaPedidosCancelados = 0

        if not dfPedidosNaoCancelados.empty:
            dfSomaPedidosNaoCancelados = len(dfPedidosNaoCancelados[dfPedidosNaoCancelados['id_empresa_cliente_id'] == row.id_cliente])
            dfClientesPedidosSomas.at[index,'soma_pedidos_nao_cancelados'] = dfSomaPedidosNaoCancelados
        else:
            dfClientesPedidosSomas.at[index,'soma_pedidos_nao_cancelados'] = dfSomaPedidosNaoCancelados

        if not dfPedidosCancelados.empty:
            dfSomaPedidosCancelados = len(dfPedidosCancelados[dfPedidosCancelados['id_empresa_cliente_id'] == row.id_cliente])
            dfClientesPedidosSomas.at[index, 'soma_pedidos_cancelados'] = dfSomaPedidosCancelados
        else:
            dfClientesPedidosSomas.at[index,'soma_pedidos_cancelados'] = dfSomaPedidosCancelados

        dfClientesPedidosSomas.at[index, 'pedidos_feitos'] = dfSomaPedidosNaoCancelados + dfSomaPedidosCancelados
    return dfClientesPedidosSomas

# Relatórios #
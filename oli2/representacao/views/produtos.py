from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .funcoes import *

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
        print(request.POST["empresa"])
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

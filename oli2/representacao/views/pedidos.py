from ..models import *
from ..forms import *
from ..functions import render_pdf_view
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .funcoes import *
import json


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

    listaPedido = Pedidos.objects.order_by('-data_pedido', '-horario_pedido')

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

    if form.is_valid():
        pedido = form.save()

        #mensagem_cadastro_sucesso(request)

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
        return HttpResponse("Ok")
    else:
        return render(request, template_name, {'id':pedido.id_pedido, 'pedido': pedido, 'representada': representada, 'produtos': produtos})


@csrf_exempt
def retorna_informacoes_itens_pedido(request, id_pedido):
    if request.is_ajax() and request.method == "POST":
        pedido = get_object_or_404(Pedidos, pk=id_pedido)
        itens_pedido = ItensPedido.objects.filter(id_pedido=pedido).select_related("id_produto").all()\
            .values(
                'id_pedido_id',
                'id_produto_id',
                'id_produto__codigo_produto',
                'id_produto__descricao',
                'id_produto__custo_unitario',
                'quantidade',
                'custo_total'
            )

        return JsonResponse({'itens_pedido': list(itens_pedido)})


@login_required
@csrf_exempt
def editar_itens_pedido(request, id_pedido, template_name='pedidos/itens_pedido_form.html'):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    representada = get_object_or_404(Empresas, pk=pedido.id_empresa_representada.id_empresa)
    produtos = Produtos.objects.filter(empresa=representada).all()

    if request.is_ajax() and request.method == "POST":
        data = request.body
        items = json.loads(data)

        ItensPedido.objects.filter(id_pedido=pedido).delete()

        total_pedido = 0

        for item_json in items:
            #item_json = json.loads(item)

            total_pedido = total_pedido + item_json['custo_total']

            item_pedido = ItensPedido(
                id_pedido=pedido,
                id_produto=get_object_or_404(Produtos, pk=item_json['id_produto_id']),
                quantidade=item_json['quantidade'],
                custo_total=item_json['custo_total']
            )

            item_pedido.save()

            pedido.total_pedido = total_pedido
            pedido.save()
        return HttpResponse("Ok")
    else:
        return render(request, template_name, {
            'id': pedido.id_pedido,
            'pedido': pedido,
            'representada': representada,
            'produtos': produtos
        })


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

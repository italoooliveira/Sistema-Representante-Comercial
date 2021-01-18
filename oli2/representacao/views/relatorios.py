from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from io import BytesIO
from .funcoes import *
import base64
import pandas as pd
import matplotlib.pyplot as plt


# Relatórios #
# Acompanhamentos #

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
        form.save()

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


# Acompanhamentos #


# Prospecções de Clientes #


@login_required
def prospeccoes_clientes(request, template_name='relatorios/prospeccao_clientes_form.html'):
    form = ProspeccoesClientesForm(request.GET or None)

    return render(request, template_name, {'form': form})


# Prospecções de Clientes #


# Clientes sem pedido #

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
        dfClientesSemPedidoComUltimoPedido = retorna_clientes_sem_pedidos_com_ultimo_pedido(dfClientesSemPedido, dfPedidosDataAnteriorInicial)

        clientes_sem_pedidos = dfClientesSemPedidoComUltimoPedido.T.to_dict().values()
        #paginator = Paginator(clientes_sem_pedidos, 15)
        #page = request.GET.get('page')
        #clientes_sem_pedidos_por_pagina = paginator.get_page(page)

        #clientes_sem_pedido_list = dfClientesSemPedidoComUltimoPedido.values.tolist()

        '''
        for item in clientes_sem_pedido_list:
            if item[1] != "":
                clientes_sem_pedido.append({'nome_fantasia': item[1], 'data_ultimo_pedido': item[-1]})
            else:
                clientes_sem_pedidos.append({'nome_fantasia': item[2], 'data_ultimo_pedido': item[-1]})
        '''
    return render(request, template_name, {'form': form, 'clientes_sem_pedidos': clientes_sem_pedidos})


def retorna_clientes_sem_pedidos_com_ultimo_pedido(dfClientesSemPedido, dfPedidos):
    for index, row in dfClientesSemPedido.iterrows():
        if not dfPedidos.empty:
            dfUltimoPedido = dfPedidos.loc[dfPedidos.id_empresa_cliente_id == row.id_cliente].tail(1)

            if not dfUltimoPedido.empty:
                dfClientesSemPedido.at[index, 'ultimo_pedido'] = dfUltimoPedido.iloc[0]['data_pedido']
            else:
                dfClientesSemPedido.at[index, 'ultimo_pedido'] = ''
        else:
            dfClientesSemPedido['ultimo_pedido'] = ''
    return dfClientesSemPedido


# Clientes sem pedido #


# Cancelamento de pedidos #

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

        if(listaPedidos):
            dfClientes = pd.DataFrame(listaClientes)
            dfPedidos = pd.DataFrame(listaPedidos)

            dfPedidosNaoCancelados = dfPedidos.loc[dfPedidos.status != "CANCELADO"]
            dfPedidosCancelados = dfPedidos.loc[dfPedidos.status == "CANCELADO"]

            dfClientesPedidosSomas = dfClientes[dfClientes['id_cliente'].isin(dfPedidos['id_empresa_cliente_id'])]
            dfClientesPedidosSomas = retorna_resultado_pedidos_cancelados(dfClientesPedidosSomas, dfPedidosNaoCancelados, dfPedidosCancelados)

            clientes_pedidos_somas = dfClientesPedidosSomas.T.to_dict().values()

            '''
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
            '''
        else:
            clientes_pedidos_somas = listaPedidos

    return render(request, template_name, {'form': form, 'clientes_pedidos_somas':clientes_pedidos_somas})


def retorna_resultado_pedidos_cancelados(dfClientesPedidosSomas, dfPedidosNaoCancelados, dfPedidosCancelados):
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


# Cancelamento de pedidos #
# Relatórios #
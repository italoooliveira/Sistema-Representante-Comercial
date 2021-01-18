from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .funcoes import *
import json


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

    paginator = Paginator(listaPrepostos, 15)
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


@csrf_exempt
def retorna_informacoes_preposto(request):
    if request.is_ajax() and request.method == "POST":
        data = request.body

        id_preposto = json.loads(data)

        empresas_prepostos = Prepostos.empresa.through.objects.filter(prepostos_id=id_preposto).all().values()

        return JsonResponse({'prepostos_empresa': list(empresas_prepostos)})


@login_required
def listar_rotas_prepostos(request, template_name='pessoas/lista_rotas_prepostos.html'):
    listaRotasPrepostos = Rotas.objects.all()

    paginator = Paginator(listaRotasPrepostos, 15)
    page = request.GET.get('page')
    rotas_prepostos_por_pagina = paginator.get_page(page)

    data = {'rotas_prepostos': rotas_prepostos_por_pagina}

    return render(request, template_name, data)


@login_required
@csrf_exempt
def cadastrar_rotas_prepostos(request, template_name='pessoas/rotas_prepostos_form.html'):
    form = RotaPrepostoForm(request.POST or None)

    if request.is_ajax() and request.method == "POST":
        data = request.body

        rota = json.loads(data)

        rt = Rotas(
            nome_rota=rota['nome_rota']
        )

        rt.save()

        prepostos = rota['prepostos']

        for preposto in prepostos:
            preposto_json = json.loads(preposto)

            rota_preposto = RotaPrepostos(
                id_rota=rt,
                id_preposto=get_object_or_404(Prepostos, pk=preposto_json['id_preposto'])
            )

            rota_preposto.save()

            clientes = preposto_json['clientes']

            for cliente in clientes:
                s = False
                t = False
                q = False
                qi = False
                sx = False
                sa = False

                for dia in cliente['dias']:
                    if (dia == "s"):
                        s = True
                    if (dia == "t"):
                        t = True
                    if (dia == "q"):
                        q = True
                    if (dia == "qi"):
                        qi = True
                    if (dia == "sx"):
                        sx = True
                    if (dia == "sa"):
                        sa = True

                preposto_cliente = PrepostoClientes(
                    id_rota_preposto=rota_preposto,
                    id_cliente=get_object_or_404(Clientes, pk=cliente['id_cliente']),
                    frequencia=cliente['frequencia'],
                    s=s,
                    t=t,
                    q=q,
                    qi=qi,
                    sx=sx,
                    sa=sa
                )

                preposto_cliente.save()

                mensagem_cadastro_sucesso(request)
        return HttpResponse("OK")
    return render(request, template_name, {'form': form})


@login_required
@csrf_exempt
def retorna_informacoes_rota_prepostos(request, id_rota):
    if request.is_ajax() and request.method == "POST":
        rota = get_object_or_404(Rotas, pk=id_rota)
        rota_prepostos = RotaPrepostos.objects.filter(id_rota=rota).all()

        prepostos = []
        rota_prepostos_clientes = {}

        for rota_preposto in rota_prepostos:
            clientes_preposto = PrepostoClientes.objects.filter(id_rota_preposto=rota_preposto).values()
            preposto = Prepostos.objects.filter(id_preposto=rota_preposto.id_preposto_id).select_related('id_usuario').first()
            prepostos.append({'id_preposto': rota_preposto.id_preposto_id, 'clientes': list(clientes_preposto), 'nome_preposto':preposto.id_usuario.nome})

        rota_prepostos_clientes['id_rota'] = rota.id_rota
        rota_prepostos_clientes['prepostos'] = list(prepostos)

        return JsonResponse({'rota_prepostos_clientes': rota_prepostos_clientes})


@login_required
@csrf_exempt
def editar_rotas_prepostos(request, id_rota, template_name='pessoas/edicao_rotas_prepostos_form.html'):
    rota = get_object_or_404(Rotas, pk=id_rota)
    form = RotaPrepostoForm(initial={'nome_rota': rota.nome_rota})

    if request.is_ajax() and request.method == "POST":
        data = request.body
        rota_json = json.loads(data)

        rota.nome_rota = rota_json['nome_rota']
        rota.save()

        RotaPrepostos.objects.filter(id_rota=rota).delete()

        prepostos = rota_json['prepostos']

        for preposto in prepostos:
            preposto_json = json.loads(preposto)

            rota_preposto = RotaPrepostos(
                id_rota=rota,
                id_preposto=get_object_or_404(Prepostos, pk=preposto_json['id_preposto'])
            )

            rota_preposto.save()

            clientes = preposto_json['clientes']

            for cliente in clientes:
                s = False
                t = False
                q = False
                qi = False
                sx = False
                sa = False

                s = cliente['s']
                t = cliente['t']
                q = cliente['q']
                qi = cliente['qi']
                sx = cliente['sx']
                sa = cliente['sa']

                preposto_cliente = PrepostoClientes(
                    id_rota_preposto=rota_preposto,
                    id_cliente=get_object_or_404(Clientes, pk=cliente['id_cliente_id']),
                    frequencia=cliente['frequencia'],
                    s=s,
                    t=t,
                    q=q,
                    qi=qi,
                    sx=sx,
                    sa=sa
                )

                preposto_cliente.save()

                mensagem_edicao_sucesso(request)
        return HttpResponse("OK")
    return render(request, template_name, {'id_rota': id_rota, 'rota': rota,'form': form})


@login_required
def excluir_rota(request, id_rota):
    rota = get_object_or_404(Rotas, pk=id_rota)

    if request.method == "GET":
        rota.delete()

        return redirect('rotas-prepostos')


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

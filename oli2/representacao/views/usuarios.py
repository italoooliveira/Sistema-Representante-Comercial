from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .funcoes import *


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

        if permissao == "ADMINISTRADOR":
            user.is_superuser = True

        user.save()

        usuario = Usuarios(nome=nome, email=email, permissao=permissao, telefone=telefone, django_auth_user=user)
        usuario.save()

        mensagem_cadastro_sucesso(request)

        if permissao == "PREPOSTO":
            preposto = Prepostos(id_usuario=usuario)
            preposto.possui_vinculo_empresa = 0
            preposto.possui_vinculo_cliente = 0
            preposto.comissao = 0
            preposto.save()

        return redirect('cadastrar-usuario')
    return render(request, template_name, {'form': form})


@login_required
def editar_usuario(request, id_usuario, template_name='usuarios/usuario_form.html'):
    usuario = get_object_or_404(Usuarios, pk=id_usuario)

    if request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']
        permissao = request.POST['permissao']
        nome = request.POST['nome']
        telefone = request.POST['telefone']

        usuario.email = email
        permissao_original = usuario.permissao
        usuario.permissao = permissao

        usuario.nome = nome
        usuario.telefone = telefone
        usuario.save()

        user = get_object_or_404(User, pk=usuario.django_auth_user.id)
        user.username = nome
        user.email = email

        if senha:
            user.set_password(senha)

        if usuario.permissao == "ADMINISTRADOR":
            user.is_superuser = True

        user.save()

        if permissao != permissao_original and permissao == "PREPOSTO":
            preposto = Prepostos(id_usuario=usuario)
            preposto.possui_vinculo_empresa = 0
            preposto.possui_vinculo_cliente = 0
            preposto.comissao = 0
            preposto.save()

        return redirect('usuarios')

    else:
        form = UsuarioFormCustom()
        form.fields['email'].initial = usuario.email
        form.fields['permissao'].initial = usuario.permissao
        form.fields['nome'].initial = usuario.nome
        form.fields['telefone'].initial = usuario.telefone

    return render(request, template_name, {'form': form})


@login_required
def excluir_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuarios, pk=id_usuario)

    if request.method == "GET":
        usuario.delete()

        user = get_object_or_404(User, pk=usuario.django_auth_user.id)
        user.delete()

        return redirect('usuarios')


# Tarefas #

@login_required
def listar_tarefas(request, template_name="usuarios/lista_tarefas.html"):
    form = PesquisaTarefaForm(request.GET or None)
    listaTarefas = Tarefas.objects.order_by('id_tarefa')
    id_user = request.user.id

    if 'descricao_tarefa' in request.GET:
        descricao_tarefa = request.GET['descricao_tarefa']

        if descricao_tarefa:
            listaTarefas = listaTarefas.filter(Q(descricao_tarefa__icontains = descricao_tarefa))

    if 'data_inicial' in request.GET:
        data_inicial = request.GET['data_inicial']

        if data_inicial:
            data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y').strftime('%Y-%m-%d')
            listaTarefas = listaTarefas.filter(data_inicial__gte = data_inicial)

    if 'data_final' in request.GET:
        data_final = request.GET['data_final']

        if data_final:
            data_final = datetime.strptime(data_final, '%d/%m/%Y').strftime('%Y-%m-%d')
            listaTarefas = listaTarefas.filter(data_final__lte = data_final)

    if 'status' in request.GET:
        status = request.GET['status']

        if status:
            listaTarefas = listaTarefas.filter(status=status)

    if 'minhas_tarefas' in request.GET:
        id_usuario = Usuarios.objects.get(id_usuario=id_user)
        listaTarefas = listaTarefas.filter(usuario__in=[id_usuario])

    listaTarefas = listaTarefas.all().values('id_tarefa', 'descricao_tarefa', 'data_inicial', 'data_final', 'status')
    paginator = Paginator(listaTarefas, 15)
    page = request.GET.get('page')
    tarefas_por_pagina = paginator.get_page(page)

    data = {'tarefas': tarefas_por_pagina, 'form': form}

    return render(request, template_name, data)


@login_required
def cadastrar_tarefa(request, template_name="usuarios/tarefas_form.html"):
    form = TarefaForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            mensagem_cadastro_sucesso(request)

            return redirect('cadastrar-tarefa')
    return render(request, template_name, {'form': form})


@login_required
def editar_tarefa(request, id_tarefa, template_name="usuarios/tarefas_form.html"):
    tarefa = get_object_or_404(Tarefas, pk=id_tarefa)

    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)

        if form.is_valid():
            form.save()
            return redirect('tarefas')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, template_name, {'form': form })

@login_required
def excluir_tarefa(request, id_tarefa):
    tarefa = get_object_or_404(Tarefas, pk=id_tarefa)

    if request.method == "GET":
        tarefa.delete()
        return redirect('tarefas')


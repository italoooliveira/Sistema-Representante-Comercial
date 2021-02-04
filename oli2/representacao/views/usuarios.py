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
        user.save()

        '''
        senha_bytes = senha.encode('ascii')
        senha_base64_bytes = base64.b64encode(senha_bytes)
        senha_base64_bytes = senha_base64_bytes.decode("ascii")
        usuario = Usuarios(nome=nome, email=email, senha=senha_base64_bytes, permissao=permissao, telefone=telefone, django_auth_user=user)
        '''

        usuario = Usuarios(nome=nome, email=email, senha=senha, permissao=permissao, telefone=telefone, django_auth_user=user)
        usuario.save()

        mensagem_cadastro_sucesso(request)

        if permissao == "PREPOSTO":
            preposto = Prepostos(id_usuario=usuario)
            preposto.possui_vinculo_empresa = 0;
            preposto.possui_vinculo_cliente = 0;
            preposto.comissao = 0;
            preposto.save()

        return redirect('cadastrar-usuario')
    return render(request, template_name, {'form': form})


@login_required
def editar_usuario(request, id_usuario, template_name='usuarios/usuario_form.html'):
    usuario = get_object_or_404(Usuarios, pk=id_usuario)

    '''
    base64_string = usuario.senha
    base64_bytes = base64_string.encode("ascii")
    senha_string_bytes = base64.b64decode(base64_bytes)
    senha_string = senha_string_bytes.decode("ascii")
    usuario.senha = senha_string
    '''

    if request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']
        permissao = request.POST['permissao']
        nome = request.POST['nome']
        telefone = request.POST['telefone']

        usuario.email = email
        permissao_original = usuario.permissao
        usuario.permissao = permissao
        '''
        senha_bytes = senha.encode('ascii')
        senha_base64_bytes = base64.b64encode(senha_bytes)
        senha_base64_bytes = senha_base64_bytes.decode("ascii")
        '''

        usuario.senha = senha
        usuario.nome = nome
        usuario.telefone = telefone
        usuario.save()

        user = get_object_or_404(User, pk=usuario.django_auth_user.id)
        user.username = nome
        user.email = email
        user.set_password(senha)
        user.save()

        if permissao != permissao_original and permissao == "PREPOSTO":
            preposto = Prepostos(id_usuario=usuario)
            preposto.possui_vinculo_empresa = 0
            preposto.possui_vinculo_cliente = 0
            preposto.comissao = 0
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
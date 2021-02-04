from django.contrib import messages


def mensagem_edicao_sucesso(request):
    messages.success(request, 'Atualizado com sucesso')


def mensagem_cadastro_sucesso(request):
    messages.success(request, 'Cadastro realizado com sucesso')


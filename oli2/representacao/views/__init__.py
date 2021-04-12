from .usuarios import *
from .empresas import *
from .pessoas import *
from .produtos import *
from .pedidos import *
from .configuracoes import *
from .relatorios import *
from .customizacoes import *


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


@login_required
def index(request, template_name='index.html'):
    cg01 = get_object_or_404(Configuracoes, pk=3)

    request.session['cg01'] = eval(cg01.valor)

    return render(request, template_name)

from rest_framework import viewsets
from representacao.models import *
from api.serializers import *
from rest_framework.permissions import AllowAny


class UsuariosViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer


class TarefasViewSet(viewsets.ModelViewSet):
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer

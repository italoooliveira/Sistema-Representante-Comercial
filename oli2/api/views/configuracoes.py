from rest_framework import viewsets
from representacao.models import *
from api.serializers import *


class ConfiguracoesViewSet(viewsets.ModelViewSet):
    queryset = Configuracoes.objects.all()
    serializer_class = ConfiguracoesSerializer

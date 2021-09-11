from rest_framework import viewsets
from representacao.models import *
from api.serializers import *


class AcompanhamentosViewSet(viewsets.ModelViewSet):
    queryset = Acompanhamentos.objects.all()
    serializer_class = AcompanhamentosSerializer


class AcompanhamentoEmpresaViewSet(viewsets.ModelViewSet):
    queryset = AcompanhamentoEmpresa.objects.all()
    serializer_class = AcompanhamentosSerializer


class AcompanhamentoPrepostoEmpresaViewSet(viewsets.ModelViewSet):
    queryset = AcompanhamentoPrepostoEmpresa.objects.all()
    serializer_class = AcompanhamentoPrepostoEmpresaSerializer

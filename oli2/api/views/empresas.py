from rest_framework import viewsets
from representacao.models import *
from api.serializers import *


class EmpresasViewSet(viewsets.ModelViewSet):
    queryset = Empresas.objects.all()
    serializer_class = EmpresasSerializer


class MinhaEmpresaViewSet(viewsets.ModelViewSet):
    queryset = MinhaEmpresa.objects.all()
    serializer_class = MinhaEmpresaSerializer


class TiposEmpresaViewSet(viewsets.ModelViewSet):
    queryset = TiposEmpresa.objects.all()
    serializer_class = TiposEmpresaSerializer


class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer

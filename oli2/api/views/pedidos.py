from rest_framework import viewsets
from representacao.models import *
from api.serializers import *


class FormasPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FormasPagamento.objects.all()
    serializer_class = FormasPagamentoSerializer


class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer


class ItensPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItensPedido.objects.all()
    serializer_class = ItensPedidoSerializer
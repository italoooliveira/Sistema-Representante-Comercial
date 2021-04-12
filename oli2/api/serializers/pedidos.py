from rest_framework import serializers
from representacao.models import *


class FormasPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormasPagamento
        fields = '__all__'


class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'


class ItensPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItensPedido
        fields = '__all__'

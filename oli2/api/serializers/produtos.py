from rest_framework import serializers
from representacao.models import *


class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'


class UnidadesVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadesVenda
        fields = '__all__'


class TiposEmbalagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposEmbalagem
        fields = '__all__'


class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'

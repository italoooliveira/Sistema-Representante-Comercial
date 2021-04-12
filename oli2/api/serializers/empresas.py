from rest_framework import serializers
from representacao.models import *


class TiposEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposEmpresa
        fields = '__all__'


class MinhaEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinhaEmpresa
        fields = '__all__'


class EmpresasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = '__all__'


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'

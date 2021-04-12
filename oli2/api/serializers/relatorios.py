from rest_framework import serializers
from representacao.models import *


class AcompanhamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acompanhamentos
        fields = '__all__'


class AcompanhamentoEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcompanhamentoEmpresa
        fields = '__all__'


class AcompanhamentoPrepostoEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcompanhamentoPrepostoEmpresa
        fields = '__all__'

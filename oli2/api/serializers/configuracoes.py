from rest_framework import serializers
from representacao.models import *


class ConfiguracoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracoes
        fields = '__all__'

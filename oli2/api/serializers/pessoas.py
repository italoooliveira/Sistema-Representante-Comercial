from rest_framework import serializers
from representacao.models import *


class PrepostosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prepostos
        fields = '__all__'


class RotasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rotas
        fields = '__all__'


class RotaPrepostosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotaPrepostos
        fields = '__all__'


class PrepostoClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrepostoClientes
        fields = '__all__'


class ContatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contatos
        fields = '__all__'

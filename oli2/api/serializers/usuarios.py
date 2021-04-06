from rest_framework import serializers
from representacao.models import *


class UsuariosSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['nome'],
            email=validated_data['email']
        )
        user.set_password(validated_data['senha'])

        if validated_data['permissao'] == 'ADMINISTRADOR':
            user.is_superuser = True

        user.save()

        usuario = Usuarios.objects.create(
            email=validated_data['email'],
            permissao=validated_data['permissao'],
            nome=validated_data['nome'],
            django_auth_user=user
        )

        if "telefone" in validated_data:
            usuario.telefone=validated_data['telefone']

        usuario.save()

        return usuario

    class Meta:
        model = Usuarios
        fields = [
            'email', 'senha', 'permissao', 'nome', 'telefone'
        ]


class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'

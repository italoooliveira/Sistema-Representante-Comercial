from django.db import models
from django.contrib.auth.models import User


class Usuarios(models.Model):
    PERMISSOES = (
        ('BASICA', 'BÁSICA'),
        ('PREPOSTO', 'PREPOSTO'),
        ('ADMINISTRADOR', 'ADMINISTRADOR'),
    )

    id_usuario = models.AutoField(primary_key=True)
    email = models.EmailField()
    senha = models.CharField(max_length=200, null=True)
    permissao = models.CharField(max_length=30, choices=PERMISSOES)
    nome = models.CharField(max_length=255, db_index=True)
    telefone = models.CharField(max_length=80, null=True, blank=True)
    django_auth_user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome
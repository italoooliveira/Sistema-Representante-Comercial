from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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


class Tarefas(models.Model):
    FREQUENCIA = (
        ('DIARIA', 'DIÁRIA'),
        ('SEMANAL', 'SEMANAL'),
        ('QUINZENAL', 'QUINZENAL'),
        ('MENSAL', 'MENSAL'),
        ('OUTRA', 'OUTRA')
    )

    STATUS = (
        ('A FAZER', 'A FAZER'),
        ('EM ANDAMENTO', 'EM ANDAMENTO'),
        ('CONCLUIDA', 'CONCLUÍDA'),
        ('REVISAO', 'REVISÃO'),
        ('CANCELADA', 'CANCELADA')
    )

    id_tarefa = models.AutoField(primary_key=True)
    usuario = models.ManyToManyField(Usuarios, blank=True)
    descricao_tarefa = models.CharField(db_index=True, max_length=255)
    data_inicial = models.DateField(default=datetime.now().date(), db_index=True)
    data_final = models.DateField(default=datetime.now().date(), null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS, default='A FAZER', db_index=True)
    observacao = models.TextField(null=True, blank=True)
    frequencia = models.CharField(max_length=30, choices=FREQUENCIA, null=True, blank=True)
    outra = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.descricao_tarefa


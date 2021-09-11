from .usuarios import Usuarios
from .empresas import Empresas, Clientes
from django.db import models


class Prepostos(models.Model):
    id_preposto = models.AutoField(primary_key=True)
    possui_vinculo_empresa = models.BooleanField()
    comissao = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=True)
    empresa = models.ManyToManyField(Empresas, null=True, blank=True)

    def __str__(self):
        return self.id_usuario.nome


class Rotas(models.Model):
    id_rota = models.AutoField(primary_key=True)
    nome_rota = models.CharField(max_length=300)


class RotaPrepostos(models.Model):
    id_rota_preposto = models.AutoField(primary_key=True)
    id_rota = models.ForeignKey(Rotas, on_delete=models.CASCADE)
    id_preposto = models.ForeignKey(Prepostos, on_delete=models.PROTECT)


class PrepostoClientes(models.Model):
    FREQUENCIA = (
        ('SEMANAL', 'SEMANAL'),
        ('QUINZENAL', 'QUINZENAL'),
        ('MENSAL', 'MENSAL'),
        ('OUTRA', 'OUTRA')
    )

    id_rota_preposto = models.ForeignKey(RotaPrepostos, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT)
    s = models.BooleanField()
    t = models.BooleanField()
    q = models.BooleanField()
    qi = models.BooleanField()
    sx = models.BooleanField()
    sa = models.BooleanField()
    frequencia = models.CharField(max_length=30, choices=FREQUENCIA, null=True, blank=True)
    outra = models.IntegerField(null=True, blank=True)


class Contatos(models.Model):
    id_contato = models.AutoField(primary_key=True)
    nome_contato = models.CharField(max_length=255, null=True, db_index=True)
    possui_vinculo_empresa = models.BooleanField()
    possui_vinculo_cliente = models.BooleanField()
    telefone = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    banco_contato = models.CharField(max_length=15, null=True, blank=True)
    agencia_contato = models.CharField(max_length=30, null=True, blank=True)
    conta_contato = models.CharField(max_length=30, null=True, blank=True)
    empresa = models.ManyToManyField(Empresas, null=True, blank=True)
    cliente = models.ManyToManyField(Clientes, null=True, blank=True)

    def __str__(self):
        return self.nome_contato
from .empresas import Empresas
from .pessoas import Prepostos
from django.db import models


class Acompanhamentos(models.Model):
    id_acompanhamento = models.AutoField(primary_key=True)
    meta_geral = models.DecimalField(max_digits=10, decimal_places=2)
    dias_uteis = models.IntegerField(default=1)
    data_inicial = models.DateField()
    data_final = models.DateField()
    dias_trabalhados = models.IntegerField(default=0)


class AcompanhamentoEmpresa(models.Model):
    id_acompanhamento = models.ForeignKey(Acompanhamentos, on_delete=models.PROTECT)
    id_empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT)
    meta_empresa = models.FloatField()


class AcompanhamentoPreposto(models.Model):
    TIPO_META = (
        ('VALOR', 'VALOR'),
        ('PORCENTAGEM', 'PORCENTAGEM')
    )

    id_acompanhamento = models.ForeignKey(Acompanhamentos, on_delete=models.PROTECT)
    id_preposto = models.ForeignKey(Prepostos, on_delete=models.PROTECT)
    tipo_meta = models.CharField(max_length=30, choices=TIPO_META, null=True)
    meta_preposto = models.FloatField()


class AcompanhamentoPrepostoEmpresa(models.Model):
    TIPO_META = (
        ('VALOR', 'VALOR'),
        ('PORCENTAGEM', 'PORCENTAGEM')
    )

    id_acompanhamento = models.ForeignKey(Acompanhamentos, on_delete=models.PROTECT)
    id_empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT)
    id_preposto = models.ForeignKey(Prepostos, on_delete=models.PROTECT)
    tipo_meta = models.CharField(max_length=30, choices=TIPO_META, null=True)
    meta_preposto_empresa = models.FloatField()
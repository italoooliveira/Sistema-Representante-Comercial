from .empresas import Empresas
from django.db import models


class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome_categoria = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nome_categoria


class UnidadesVenda(models.Model):
    id_unidade_venda = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.sigla


class TiposEmbalagem(models.Model):
    id_tipo_embalagem = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.tipo


class Produtos(models.Model):
    id_produto = models.AutoField(primary_key=True)
    codigo_produto = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    descricao = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    custo_unitario = models.FloatField(default=0, blank=True)
    comissao = models.FloatField(default=0, blank=True)
    ipi = models.FloatField(default=0, blank=True)
    aliquota = models.FloatField(default=0, blank=True)
    reducao_icms = models.FloatField(default=0, blank=True)
    st = models.FloatField(default=0, blank=True)
    pis = models.FloatField(default=0, blank=True)
    mva_st = models.FloatField(default=0, blank=True)
    quantidade_embalagem = models.FloatField(default=0, blank=True)
    validade = models.IntegerField(default=0, blank=True)
    imagem = models.ImageField(null=True, blank=True, upload_to='produtos/')
    ean = models.FloatField(default=0, blank=True)
    dun = models.FloatField(default=0, blank=True)
    preco_embalagem = models.FloatField(default=0, blank=True)
    possui_multiplo_venda = models.BooleanField()
    multiplo = models.IntegerField(default=0, blank=True)
    preco_total = models.FloatField()
    id_unidade_venda = models.ForeignKey(UnidadesVenda, on_delete=models.PROTECT)
    id_tipo_embalagem = models.ForeignKey(TiposEmbalagem, on_delete=models.PROTECT)
    id_categoria = models.ForeignKey(Categorias, on_delete=models.PROTECT)
    empresa = models.ManyToManyField(Empresas)

    def __str__(self):
        return self.descricao
from .usuarios import Usuarios
from .empresas import Empresas, Clientes
from .pessoas import Contatos
from .produtos import Produtos
from django.db import models
from datetime import datetime


class FormasPagamento(models.Model):
    id_forma_pagamento = models.AutoField(primary_key=True)
    nome_forma_pagamento = models.CharField(max_length=80, null=True)
    prazo = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nome_forma_pagamento + ' - ' + self.prazo


class Pedidos(models.Model):
    STATUS = (
        ('AGUARDANDO FATURAMENTO', 'AGUARDANDO FATURAMENTO'),
        ('FATURADO', 'FATURADO'),
        ('CANCELADO', 'CANCELADO'),
    )

    id_pedido = models.AutoField(primary_key=True)
    numero_pedido = models.CharField(max_length=50, null=True, db_index=True)
    observacao = models.TextField(null=True, blank=True)
    total_pedido = models.FloatField(default=0, blank=True)
    data_pedido = models.DateField(default=datetime.now().date(), null=True, db_index=True)
    data_entrega = models.DateField(null=True, blank=True, db_index=True)
    ordem_compra = models.CharField(max_length=50, null=True, db_index=True)
    status = models.CharField(max_length=30, choices=STATUS, default='AGUARDANDO FATURAMENTO', null=True, blank=True)
    id_empresa_representada = models.ForeignKey(Empresas, on_delete=models.PROTECT, related_name="fk_empresa_representada", db_index=True)
    id_empresa_cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT, related_name="fk_empresa_cliente", db_index=True)
    id_forma_pagamento = models.ForeignKey(FormasPagamento, on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT)
    id_contato = models.ForeignKey(Contatos, on_delete=models.PROTECT)


class ItensPedido(models.Model):
    id_item_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.PROTECT)
    id_produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
    quantidade = models.FloatField()
    custo_total = models.FloatField()
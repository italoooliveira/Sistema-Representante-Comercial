from .usuarios import Usuarios
from django.db import models


class TiposEmpresa(models.Model):
    id_tipo_empresa = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.tipo


class MinhaEmpresa(models.Model):
    TIPO_IE_CHOICES = (
        ('CONTRIBUINTE', 'CONTRIBUINTE'),
        ('NAO CONTRIBUINTE', 'NÃO CONTRIBUINTE'),
        ('ISENTO', 'ISENTO'),
    )

    id_minha_empresa = models.AutoField(primary_key=True)
    logo = models.ImageField(null=True, blank=True, upload_to='minha-empresa/')
    razao_social = models.CharField(max_length=255, null=True, db_index=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    cnpj = models.CharField(max_length=25, null=True, blank=True, db_index=True)
    tipo_ie = models.CharField(max_length=30, choices=TIPO_IE_CHOICES, null=True)
    inscricao_estadual = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    telefone = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_nfe = models.EmailField(null=True, blank=True)
    endereco = models.CharField(max_length=80, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=80, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    cidade = models.CharField(max_length=150, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)


class Empresas(models.Model):
    TIPO_IE_CHOICES = (
        ('CONTRIBUINTE', 'CONTRIBUINTE'),
        ('NAO CONTRIBUINTE', 'NÃO CONTRIBUINTE'),
        ('ISENTO', 'ISENTO'),
    )

    id_empresa = models.AutoField(primary_key=True)
    logo = models.ImageField(null=True, blank=True, upload_to='empresas/')
    razao_social = models.CharField(max_length=255, null=True, db_index=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    cnpj = models.CharField(max_length=25, null=True, blank=True, db_index=True)
    tipo_ie = models.CharField(max_length=30, choices=TIPO_IE_CHOICES, null=True)
    inscricao_estadual = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    telefone = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_nfe = models.EmailField(null=True, blank=True)
    endereco = models.CharField(max_length=80, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=80, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    cidade = models.CharField(max_length=150, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    possui_pedido_minimo = models.BooleanField()
    pedido_minimo = models.FloatField(null=True, blank=True)
    possui_horario_pedido = models.BooleanField()
    horario_pedido = models.TimeField(null=True, blank=True)
    comissao = models.DecimalField(default=0, null=True, blank=True, max_digits=5, decimal_places=2)
    banco_empresa = models.CharField(max_length=15, null=True, blank=True)
    agencia_empresa = models.CharField(max_length=30, null=True, blank=True)
    conta_empresa = models.CharField(max_length=30, null=True, blank=True)
    id_tipo_empresa = models.ForeignKey(TiposEmpresa, on_delete=models.PROTECT)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.nome_fantasia:
            return self.nome_fantasia
        else:
            return ''


class Clientes(models.Model):
    TIPO_IE_CHOICES = (
        ('CONTRIBUINTE', 'CONTRIBUINTE'),
        ('NAO CONTRIBUINTE', 'NÃO CONTRIBUINTE'),
        ('ISENTO', 'ISENTO'),
    )

    id_cliente = models.AutoField(primary_key=True)
    logo = models.ImageField(null=True, blank=True, upload_to='clientes/')
    razao_social = models.CharField(max_length=255, null=True, db_index=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    cnpj = models.CharField(max_length=25, db_index=True)
    tipo_ie = models.TextField(max_length=30, choices=TIPO_IE_CHOICES, null=True, blank=True)
    inscricao_estadual = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    telefone = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_nfe = models.EmailField(null=True, blank=True)
    endereco = models.CharField(max_length=80, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=80, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    cidade = models.CharField(max_length=150, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    banco_cliente = models.CharField(max_length=15, null=True, blank=True)
    agencia_cliente = models.CharField(max_length=30, null=True, blank=True)
    conta_cliente = models.CharField(max_length=30, null=True, blank=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=True, blank=True)
    prospectado_por_usuario = models.BooleanField()

    def __str__(self):
        if self.nome_fantasia:
            return self.nome_fantasia
        else:
            return ''

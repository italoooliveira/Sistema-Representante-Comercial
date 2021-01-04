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
    razao_social = models.CharField(max_length=255, null=True, blank=True, db_index=True)
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
    razao_social = models.CharField(max_length=255, null=True, blank=True, db_index=True)
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
    comissao = models.FloatField(null=True, blank=True)
    banco_empresa = models.CharField(max_length=15, null=True, blank=True)
    agencia_empresa = models.CharField(max_length=30, null=True, blank=True)
    conta_empresa = models.CharField(max_length=30, null=True, blank=True)
    id_tipo_empresa = models.ForeignKey(TiposEmpresa, on_delete=models.PROTECT)

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
    razao_social = models.CharField(max_length=255, null=True, blank=True, db_index=True)
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


class Prepostos(models.Model):
    id_preposto = models.AutoField(primary_key=True)
    possui_vinculo_empresa = models.BooleanField()
    possui_vinculo_cliente = models.BooleanField()
    comissao = models.FloatField(blank=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=True)
    empresa = models.ManyToManyField(Empresas, null=True, blank=True)
    cliente = models.ManyToManyField(Clientes, null=True, blank=True)


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
    nome_contato = models.CharField(max_length=255, null=True, blank=True, db_index=True)
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


class Acompanhamentos(models.Model):
    id_acompanhamento = models.AutoField(primary_key=True)
    meta_geral = models.FloatField()
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
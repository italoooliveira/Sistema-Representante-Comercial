# Generated by Django 2.2.6 on 2020-11-17 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0053_delete_tipospessoa'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtos',
            name='preco_total',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contatos',
            name='cliente',
            field=models.ManyToManyField(blank=True, null=True, to='representacao.Clientes'),
        ),
        migrations.AlterField(
            model_name='contatos',
            name='empresa',
            field=models.ManyToManyField(blank=True, null=True, to='representacao.Empresas'),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='data_pedido',
            field=models.DateField(default=datetime.date(2020, 11, 17), null=True),
        ),
        migrations.AlterField(
            model_name='prepostos',
            name='cliente',
            field=models.ManyToManyField(blank=True, null=True, to='representacao.Clientes'),
        ),
        migrations.AlterField(
            model_name='prepostos',
            name='empresa',
            field=models.ManyToManyField(blank=True, null=True, to='representacao.Empresas'),
        ),
    ]
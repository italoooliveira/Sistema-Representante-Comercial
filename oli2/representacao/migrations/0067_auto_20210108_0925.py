# Generated by Django 2.2.6 on 2021-01-08 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0066_auto_20201224_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prepostos',
            name='cliente',
        ),
        migrations.AddField(
            model_name='itenspedido',
            name='custo_unitario',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itenspedido',
            name='custo_unitario_original',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='data_pedido',
            field=models.DateField(db_index=True, default=datetime.date(2021, 1, 8), null=True),
        ),
    ]
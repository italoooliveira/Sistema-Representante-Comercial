# Generated by Django 2.2.6 on 2021-02-12 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0075_auto_20210211_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minhaempresa',
            name='razao_social',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='data_pedido',
            field=models.DateField(db_index=True, default=datetime.date(2021, 2, 12)),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='horario_pedido',
            field=models.TimeField(blank=True, default=datetime.time(11, 23, 44, 131819)),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='data_final',
            field=models.DateField(blank=True, default=datetime.date(2021, 2, 12), null=True),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='data_inicial',
            field=models.DateField(db_index=True, default=datetime.date(2021, 2, 12)),
        ),
    ]
# Generated by Django 2.2.6 on 2021-03-22 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0081_auto_20210212_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracoes',
            fields=[
                ('id_configuracoes', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('valor', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='data_pedido',
            field=models.DateField(db_index=True, default=datetime.date(2021, 3, 22)),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='horario_pedido',
            field=models.TimeField(blank=True, default=datetime.time(14, 3, 12, 904582)),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='data_final',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='data_inicial',
            field=models.DateField(db_index=True, default=datetime.date(2021, 3, 22)),
        ),
    ]

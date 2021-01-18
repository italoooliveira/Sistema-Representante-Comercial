# Generated by Django 2.2.6 on 2020-11-13 15:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0050_auto_20201106_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='id_contato',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='representacao.Contatos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='data_pedido',
            field=models.DateField(default=datetime.date(2020, 11, 13), null=True),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='horario_pedido',
            field=models.TimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/'),
        ),
    ]
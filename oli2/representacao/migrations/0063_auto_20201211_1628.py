# Generated by Django 2.2.6 on 2020-12-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0062_acompanhamentos_dias_trabalhados'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='total_pedido',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='acompanhamentos',
            name='dias_uteis',
            field=models.IntegerField(default=1),
        ),
    ]
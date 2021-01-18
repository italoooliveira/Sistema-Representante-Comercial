# Generated by Django 2.2.6 on 2020-10-19 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0018_clientes_prospectado_por_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='id_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='representacao.Usuarios'),
            preserve_default=False,
        ),
    ]
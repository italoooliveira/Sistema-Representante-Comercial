# Generated by Django 2.2.6 on 2020-10-28 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0037_acompanhamentopreposto_tipo_meta'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcompanhamentoPrepostoEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_meta', models.CharField(choices=[('VALOR', 'VALOR'), ('PORCENTAGEM', 'PORCENTAGEM')], max_length=30, null=True)),
                ('meta_preposto_empresa', models.FloatField()),
                ('id_acompanhamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='representacao.Acompanhamentos')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='representacao.Empresas')),
                ('id_preposto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='representacao.Prepostos')),
            ],
        ),
    ]
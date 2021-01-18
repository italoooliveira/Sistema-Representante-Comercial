# Generated by Django 2.2.6 on 2020-10-12 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0005_auto_20201011_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoas',
            name='cargo',
        ),
        migrations.AddField(
            model_name='pessoas',
            name='informar_dados_bancarios',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='pessoas',
            name='possui_vinculo_empresa',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='pessoas',
            name='agencia',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pessoas',
            name='aniversario',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pessoas',
            name='banco',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pessoas',
            name='conta',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pessoas',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='pessoas',
            name='nome_pessoa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pessoas',
            name='telefone',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
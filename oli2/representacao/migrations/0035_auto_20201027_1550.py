# Generated by Django 2.2.6 on 2020-10-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0034_auto_20201023_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='empresas',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
# Generated by Django 2.2.6 on 2020-10-30 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representacao', '0039_remove_usuarios_senha'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='senha',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
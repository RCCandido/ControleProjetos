# Generated by Django 5.0.7 on 2024-09-21 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_alter_empresa_cidade_alter_empresa_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='cep',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='CEP'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='complemento',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Complemento'),
        ),
    ]

# Generated by Django 5.0.7 on 2024-09-21 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_empresa_bairro_empresa_cep_empresa_complemento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='bairro',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Bairro'),
        ),
    ]

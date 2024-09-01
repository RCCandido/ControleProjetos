# Generated by Django 5.0.7 on 2024-09-01 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_niveis_options_empresa_cidade_empresa_cnpj_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empresa',
            options={'ordering': ('codigo',), 'verbose_name_plural': 'Empresas'},
        ),
        migrations.RemoveField(
            model_name='empresa',
            name='id',
        ),
        migrations.AlterField(
            model_name='empresa',
            name='codigo',
            field=models.CharField(max_length=6, primary_key=True, serialize=False, unique=True, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='dados_bancarios',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Informações Bancarias'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='endereco',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='imposto',
            field=models.IntegerField(default=0, verbose_name='% Imposto'),
        ),
    ]
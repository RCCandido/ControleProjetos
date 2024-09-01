# Generated by Django 5.0.7 on 2024-09-01 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_cliente'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='niveis',
            options={'ordering': ('descricao',), 'verbose_name_plural': 'Niveis'},
        ),
        migrations.AddField(
            model_name='empresa',
            name='cidade',
            field=models.CharField(default='', max_length=80, verbose_name='Cidade'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='cnpj',
            field=models.CharField(default='', max_length=14, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='dados_bancarios',
            field=models.TextField(default='', verbose_name='Informações Bancarias'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='endereco',
            field=models.CharField(default='', max_length=250, verbose_name='Endereço'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='estado',
            field=models.CharField(default='', max_length=2, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='imposto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefone',
            field=models.CharField(default='', max_length=20, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('1', 'Cliente'), ('2', 'Colaborador')], max_length=1, verbose_name='Tipo'),
        ),
    ]

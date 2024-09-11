# Generated by Django 5.0.7 on 2024-09-11 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_servicos_comissao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='comissao',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='valor_fixo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='imposto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='% Imposto'),
        ),
    ]

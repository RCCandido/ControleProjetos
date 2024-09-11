# Generated by Django 5.0.7 on 2024-09-10 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_colaborador_comissao_alter_servicos_comissao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicos',
            name='base_comissao',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Base Comissao'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='custo_operacional',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Custo Operacional'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='desconto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='% Desconto'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='horas_especificacao',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Horas Especificação'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='horas_execucao',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Horas Execução'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='horas_save',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Horas Save'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='horas_tecnicas',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Horas Técnicas'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='imposto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='% Imposto'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='liquido',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Liquido'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='parcelamento',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Parcelamento'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='valor_bruto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Valor Bruto'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='valor_comissao',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Valor Comissao'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='valor_desconto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='R$ Desconto'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='valor_imposto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='R$ Imposto'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='valor_recebido',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Valor Recebido'),
        ),
    ]
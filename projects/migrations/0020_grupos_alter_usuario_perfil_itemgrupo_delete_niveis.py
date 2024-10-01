# Generated by Django 5.0.7 on 2024-09-30 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_alter_servicos_parcelas_alter_servicos_versao_valida'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupos',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Ativo ?')),
                ('grupo_id', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=200, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Grupos de Acesso',
                'ordering': ('grupo_id', 'descricao'),
            },
        ),
        migrations.AlterField(
            model_name='usuario',
            name='perfil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.grupos'),
        ),
        migrations.CreateModel(
            name='ItemGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rotina', models.CharField(choices=[('0', 'Todas'), ('1', 'Empresas'), ('2', 'Grupos'), ('3', 'Usuários'), ('4', 'Serviços')], max_length=80, verbose_name='Rotina')),
                ('inclusao', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Incluir')),
                ('edicao', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Editar')),
                ('exclusao', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Excluir')),
                ('logs', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Logs')),
                ('filtro', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Filtro')),
                ('item_grupo_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.grupos')),
            ],
            options={
                'verbose_name_plural': 'Item do Grupo',
                'ordering': ('created_at',),
            },
        ),
        migrations.DeleteModel(
            name='Niveis',
        ),
    ]
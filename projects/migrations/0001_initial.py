# Generated by Django 5.0.7 on 2024-09-10 17:52

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Cliente ativo ?')),
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('cnpj', models.CharField(max_length=14, verbose_name='CNPJ')),
                ('ie', models.CharField(blank=True, max_length=14, verbose_name='IE')),
                ('endereco', models.CharField(blank=True, max_length=150, verbose_name='Endereco')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=50, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=50, verbose_name='Cidade')),
                ('estado', models.CharField(choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], default='', max_length=2, verbose_name='Estado')),
                ('email', models.CharField(default='', max_length=100, verbose_name='E-mail')),
                ('email_cat', models.CharField(default='', max_length=100, verbose_name='E-mail Cat')),
                ('usa_email_cat', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='', max_length=1, verbose_name='Recebe E-mail Cat?')),
                ('telefone', models.CharField(default='', max_length=20, verbose_name='Telefone')),
                ('contatos', models.TextField(blank=True, default='', null=True, verbose_name='Contatos')),
                ('dados_bancarios', models.TextField(blank=True, default='', null=True, verbose_name='Informações Bancárias')),
                ('observacoes', models.TextField(blank=True, default='', null=True, verbose_name='Observações')),
                ('valor_hora_atual', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('perc_desconto_atual', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
            ],
            options={
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Colaborador ativo ?')),
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF')),
                ('endereco', models.CharField(blank=True, default='', max_length=250, verbose_name='Endereço')),
                ('cidade', models.CharField(default='', max_length=80, verbose_name='Cidade')),
                ('bairro', models.CharField(blank=True, max_length=50, verbose_name='Bairro')),
                ('estado', models.CharField(choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, verbose_name='Estado')),
                ('telefone', models.CharField(default='', max_length=20, verbose_name='Telefone')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('dados_bancarios', models.TextField(blank=True, default='', null=True, verbose_name='Informações Bancarias')),
                ('valor_hora', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('valor_fixo', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('comissao', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('funcao', models.CharField(choices=[('1', 'Arquiteto'), ('2', 'Analista'), ('3', 'Desenvolvedor'), ('4', 'Gerente de Projetos'), ('5', 'QA'), ('6', 'Gerente Geral'), ('7', 'Diretor')], max_length=20, verbose_name='Função')),
                ('periodo_lancamento', models.DateField(blank=True, null=True, verbose_name='Periodo Lancto')),
            ],
            options={
                'verbose_name_plural': 'Colaboradores',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Empresa ativa ?')),
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, verbose_name='Empresa')),
                ('cnpj', models.CharField(default='', max_length=18, verbose_name='CNPJ')),
                ('endereco', models.CharField(blank=True, default='', max_length=250, verbose_name='Endereço')),
                ('cidade', models.CharField(default='', max_length=80, verbose_name='Cidade')),
                ('estado', models.CharField(choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, verbose_name='Estado')),
                ('telefone', models.CharField(default='', max_length=20, verbose_name='Telefone')),
                ('dados_bancarios', models.TextField(blank=True, default='', null=True, verbose_name='Informações Bancarias')),
                ('imposto', models.FloatField(verbose_name='imposto')),
            ],
            options={
                'verbose_name_plural': 'Empresas',
                'ordering': ('codigo',),
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('processo', models.CharField(max_length=80, verbose_name='Rotina')),
                ('usuario', models.CharField(max_length=200, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('log_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='Niveis',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Nível ativo ?')),
                ('nivel_id', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=200, verbose_name='Descrição')),
                ('rotina', models.CharField(choices=[('0', 'Todas'), ('1', 'Empresas'), ('2', 'Projetos'), ('3', 'Niveis'), ('4', 'Usuários'), ('5', 'Serviços'), ('6', 'Relatórios')], max_length=80, verbose_name='Rotina')),
                ('inclusao', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Incluir')),
                ('edicao', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Editar')),
                ('exclusao', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Excluir')),
                ('logs', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Logs')),
                ('filtro', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Filtro')),
            ],
            options={
                'verbose_name_plural': 'Niveis',
                'ordering': ('nivel_id', 'descricao'),
            },
        ),
        migrations.CreateModel(
            name='Valores',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Registro ativo ?')),
                ('valor_id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('Empresa', 'Empresa'), ('Colaborador', 'Colaborador'), ('Cliente', 'Cliente'), ('Servico', 'Servico')], max_length=20, verbose_name='Tipo')),
                ('codigo', models.CharField(max_length=6, verbose_name='Codigo')),
                ('data', models.DateField(auto_now=True, verbose_name='Data')),
                ('valor_hora', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Valor Hora')),
                ('valor_fixo', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Valor Fixo')),
                ('comissao', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='% Comissão')),
                ('imposto', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='% Imposto')),
                ('desconto', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='% Desconto')),
                ('observacao', models.TextField(verbose_name='Observações')),
            ],
            options={
                'verbose_name_plural': 'Valores',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Usuário ativo ?')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=20, verbose_name='Primeiro Nome')),
                ('name', models.CharField(max_length=200, verbose_name='Nome Completo')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('password', models.CharField(max_length=30, verbose_name='Senha')),
                ('password2', models.CharField(max_length=30, verbose_name='Confirmação da Senha')),
                ('tipo', models.CharField(choices=[('1', 'Cliente'), ('2', 'Colaborador')], max_length=1, verbose_name='Tipo')),
                ('resetpsw', models.BooleanField(default=True, verbose_name='Altera Senha ?')),
                ('usefilter', models.BooleanField(default=True, verbose_name='Permite o uso de Filtros ?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('perfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.niveis')),
            ],
            options={
                'verbose_name_plural': 'Usuários',
                'ordering': ('user_id',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Projetos',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Projeto ativo ?')),
                ('codigo', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Descrição')),
                ('responsavel', models.CharField(max_length=50, verbose_name='Responsável')),
                ('arquiteto', models.CharField(max_length=50, verbose_name='Arquiteto')),
                ('data_inicio', models.DateField(blank=True, null=True, verbose_name='Inicio')),
                ('data_entrega', models.DateField(blank=True, null=True, verbose_name='Entrega')),
                ('desenvolvedor', models.CharField(max_length=50, verbose_name='Desenvolvedor')),
                ('status', models.CharField(choices=[('0', 'Orçamento'), ('1', 'Aprovado'), ('2', 'Iniciado'), ('3', 'Em Desenvolvimento'), ('4', 'Em Teste'), ('5', 'Em Homologação'), ('6', 'Homologado'), ('7', 'Em Produção'), ('8', 'Finalizado')], max_length=1, verbose_name='Status')),
                ('qtd_horas_apontadas', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('qtd_horas_projeto', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('valor_hora', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('valor_total', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.cliente')),
            ],
            options={
                'verbose_name_plural': 'Projetos',
            },
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('codigo', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=80, verbose_name='Descrição')),
                ('versao', models.CharField(max_length=3, verbose_name='Versão')),
                ('tipo', models.CharField(choices=[('Pontual', 'Pontual'), ('Sustentação', 'Sustentação'), ('Service Desk', 'Service Desk'), ('Projeto', 'Projeto'), ('Hora Adicional', 'Hora Adicional')], max_length=20, verbose_name='Tipo')),
                ('valor_hora', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor Hora')),
                ('comissao', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Comissão')),
                ('imposto', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True, verbose_name='% Imposto')),
                ('valor_imposto', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='R$ Imposto')),
                ('horas_especificacao', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Horas Especificação')),
                ('horas_tecnicas', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Horas Técnicas')),
                ('valor_bruto', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Valor Bruto')),
                ('desconto', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True, verbose_name='% Desconto')),
                ('valor_desconto', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='R$ Desconto')),
                ('valor_recebido', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Valor Recebido')),
                ('base_comissao', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Base Comissao')),
                ('valor_comissao', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Valor Comissao')),
                ('custo_operacional', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Custo Operacional')),
                ('liquido', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Liquido')),
                ('horas_save', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Horas Save')),
                ('horas_execucao', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Horas Execução')),
                ('etapa_comercial', models.CharField(choices=[('Oportunidade', 'Oportunidade'), ('Proposta', 'Proposta'), ('Fechado', 'Fechado'), ('Perdido', 'Perdido')], max_length=30, verbose_name='Etapa Comercial')),
                ('etapa_tecnica', models.CharField(choices=[('DOS16', 'DOS16'), ('Definição de Analista', 'Definição de Analista'), ('Repasse', 'Repasse'), ('Desenvolvimento', 'Desenvolvimento'), ('Validação', 'Validação'), ('Revisão', 'Revisão'), ('Acompanhamento', 'Acompanhamento'), ('Finalizado', 'Finalizado'), ('Outros', 'Outros')], max_length=30, verbose_name='Etapa Técnica')),
                ('justificativa', models.TextField(verbose_name='Justificativa')),
                ('anotacoes', models.TextField(verbose_name='Anotações')),
                ('versao_valida', models.CharField(max_length=3, verbose_name='Versão Valida')),
                ('parcelamento', models.CharField(max_length=50, verbose_name='Parcelamento')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.cliente')),
            ],
            options={
                'verbose_name_plural': 'Serviços',
            },
        ),
    ]

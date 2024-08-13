# Generated by Django 5.0.7 on 2024-08-13 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_usuario_options_usuario_resetpsw'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='username',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='user_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
# Generated by Django 5.0.7 on 2024-10-10 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_alter_itemgrupo_item_grupo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemgrupo',
            name='item_grupo_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.grupos'),
        ),
    ]
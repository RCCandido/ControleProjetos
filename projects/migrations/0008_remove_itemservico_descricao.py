# Generated by Django 5.0.7 on 2024-09-12 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_itemservico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemservico',
            name='descricao',
        ),
    ]

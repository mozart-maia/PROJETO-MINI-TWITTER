# Generated by Django 4.2.1 on 2023-05-28 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_alter_publicacao_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicacao',
            old_name='usuario',
            new_name='autor',
        ),
    ]

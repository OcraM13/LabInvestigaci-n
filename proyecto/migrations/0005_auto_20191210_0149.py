# Generated by Django 2.2.7 on 2019-12-10 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_auto_20191203_1155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentario',
            old_name='comentario',
            new_name='text_comentario',
        ),
    ]

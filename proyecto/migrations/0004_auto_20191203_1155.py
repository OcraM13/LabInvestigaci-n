# Generated by Django 2.2.7 on 2019-12-03 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0003_auto_20191203_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

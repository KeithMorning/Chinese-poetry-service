# Generated by Django 2.0.2 on 2018-03-01 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0003_auto_20180301_1504'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poem',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='poetry',
            old_name='author_id',
            new_name='author',
        ),
    ]

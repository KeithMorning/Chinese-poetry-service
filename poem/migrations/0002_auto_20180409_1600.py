# Generated by Django 2.0.2 on 2018-04-09 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorate_peotry',
            field=models.ManyToManyField(to='poem.Poetry'),
        ),
        migrations.AddField(
            model_name='user',
            name='favorate_poem',
            field=models.ManyToManyField(to='poem.Poem'),
        ),
    ]

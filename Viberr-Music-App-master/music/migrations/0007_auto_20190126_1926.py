# Generated by Django 2.1.5 on 2019-01-26 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_auto_20190126_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='is_favorite',
        ),
        migrations.RemoveField(
            model_name='song',
            name='is_favorite',
        ),
    ]

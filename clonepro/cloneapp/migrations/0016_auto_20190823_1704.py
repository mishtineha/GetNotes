# Generated by Django 2.2.2 on 2019-08-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloneapp', '0015_auto_20190821_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videos',
            name='score',
        ),
        migrations.AddField(
            model_name='videos',
            name='viewed_user',
            field=models.CharField(default='default', max_length=30),
        ),
    ]

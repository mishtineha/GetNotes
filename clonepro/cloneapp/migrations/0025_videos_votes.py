# Generated by Django 2.2.2 on 2019-10-17 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloneapp', '0024_delete_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]

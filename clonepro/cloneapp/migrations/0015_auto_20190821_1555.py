# Generated by Django 2.2.2 on 2019-08-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloneapp', '0014_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
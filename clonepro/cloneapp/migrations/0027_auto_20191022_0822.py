# Generated by Django 2.2.2 on 2019-10-22 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloneapp', '0026_liked_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=300),
        ),
    ]
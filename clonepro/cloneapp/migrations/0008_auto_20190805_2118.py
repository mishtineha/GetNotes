# Generated by Django 2.2.2 on 2019-08-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloneapp', '0007_auto_20190805_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='videofile',
            field=models.ImageField(null=True, upload_to='videos', verbose_name=''),
        ),
    ]

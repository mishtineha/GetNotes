# Generated by Django 2.2.2 on 2019-08-05 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloneapp', '0003_auto_20190805_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='videofile',
            field=models.FileField(null=True, upload_to='videos/', verbose_name=''),
        ),
    ]
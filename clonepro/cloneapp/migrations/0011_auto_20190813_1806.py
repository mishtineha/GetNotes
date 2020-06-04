# Generated by Django 2.2.2 on 2019-08-13 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cloneapp', '0010_auto_20190813_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Liked_video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_user', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('videoliked', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cloneapp.Videos')),
            ],
        ),
    ]

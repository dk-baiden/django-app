# Generated by Django 3.2.7 on 2021-10-16 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20211015_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='apps',
            field=models.ManyToManyField(to='api.AppsModel'),
        ),
    ]

# Generated by Django 3.2.19 on 2023-05-23 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0121_auto_20230523_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='configuration',
        ),
        migrations.RemoveField(
            model_name='project',
            name='topic',
        ),
        migrations.AddField(
            model_name='projecttopic',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 5, 23, 15, 57, 46, 798827), verbose_name='creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttopic',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modification date'),
        ),
    ]
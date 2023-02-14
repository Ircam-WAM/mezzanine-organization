# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-02-12 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0108_auto_20221026_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='banner_crop_data',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/images/'),
        ),
    ]

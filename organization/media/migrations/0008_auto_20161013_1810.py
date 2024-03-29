# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-13 16:10
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_media', '0007_auto_20161013_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ('created',), 'verbose_name': 'media', 'verbose_name_plural': 'medias'},
        ),
        migrations.RemoveField(
            model_name='media',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='mediatranscoded',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, verbose_name='file'),
        ),
    ]

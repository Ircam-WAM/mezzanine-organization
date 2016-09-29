# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-29 11:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-media', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VideoCategory',
            new_name='MediaCategory',
        ),
        migrations.AlterModelOptions(
            name='mediacategory',
            options={'verbose_name': 'media category', 'verbose_name_plural': 'media categories'},
        ),
        migrations.AddField(
            model_name='audio',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audios', to='organization-media.MediaCategory', verbose_name='category'),
        ),
    ]

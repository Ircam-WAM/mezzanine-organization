# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-28 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_agenda', '0004_eventaudio_eventvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventaudio',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured')], max_length=64, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='eventimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured')], max_length=64, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='eventvideo',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured')], max_length=64, verbose_name='type'),
        ),
    ]

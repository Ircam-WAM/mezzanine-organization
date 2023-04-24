# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-04-24 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0114_auto_20181002_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationimage',
            name='crop_data',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='personimage',
            name='crop_data',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='organizationimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_back', 'logo back'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('hero', 'hero'), ('banner', 'banner')], max_length=64, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='personimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_back', 'logo back'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('hero', 'hero'), ('banner', 'banner')], max_length=64, verbose_name='type'),
        ),
    ]

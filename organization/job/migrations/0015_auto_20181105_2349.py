# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-05 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-job', '0014_auto_20180924_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidacyimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('header__responsive-logo-footer', 'responsive logo footer'), ('header__responsive-frame-video', 'responsive frame video')], max_length=64, verbose_name='type'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-28 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_agenda', '0034_auto_20190130_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlink',
            name='url_en',
            field=models.URLField(blank=True, max_length=512, null=True, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='eventlink',
            name='url_fr',
            field=models.URLField(blank=True, max_length=512, null=True, verbose_name='URL'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-06-07 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0020_homeimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeimage',
            name='url',
            field=models.URLField(blank=True, max_length=512, verbose_name='URL'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-09-14 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-pages', '0043_custompage_separator'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompage',
            name='display_content',
            field=models.BooleanField(default=True, verbose_name='display content'),
        ),
    ]

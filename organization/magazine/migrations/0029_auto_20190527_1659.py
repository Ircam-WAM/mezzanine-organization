# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-27 16:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-magazine', '0028_merge_20190524_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magazine',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='magazine',
            name='title_fr',
        ),
    ]

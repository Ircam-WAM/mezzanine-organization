# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-12 11:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-pages', '0033_merge_20181116_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeimage',
            name='credits_fr',
        ),
        migrations.RemoveField(
            model_name='homeimage',
            name='title_fr',
        ),
        migrations.RemoveField(
            model_name='pageimage',
            name='credits_fr',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-11-07 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-shop', '0017_productkeyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='productkeyword',
            name='title_en',
            field=models.CharField(max_length=500, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='productkeyword',
            name='title_fr',
            field=models.CharField(max_length=500, null=True, verbose_name='Title'),
        ),
    ]
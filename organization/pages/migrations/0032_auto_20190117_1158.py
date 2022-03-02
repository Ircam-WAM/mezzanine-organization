# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-17 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-pages', '0031_dynamicmultimediapage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='_meta_title',
            field=models.CharField(blank=True, help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Meta title'),
        ),
    ]

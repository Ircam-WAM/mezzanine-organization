# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-24 08:58
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_magazine', '0006_auto_20160924_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='brief',
            name='content_fr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
    ]

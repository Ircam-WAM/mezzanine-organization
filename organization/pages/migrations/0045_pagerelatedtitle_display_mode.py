# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-09-14 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0044_custompage_display_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagerelatedtitle',
            name='display_mode',
            field=models.CharField(choices=[('0', 'Display full width block without nav menu at left'), ('1', 'Display as width limited block with nav menu at left')], default='0', max_length=1),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-06-15 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0143_auto_20190703_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_referenced',
            field=models.BooleanField(default=True, help_text='Determine if the Person has to be referenced on search', verbose_name='Is Referenced'),
        ),
    ]

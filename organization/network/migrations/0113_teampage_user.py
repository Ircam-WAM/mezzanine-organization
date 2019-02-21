# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-08-24 10:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization-network', '0112_auto_20180502_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='teampage',
            name='user',
            field=models.ForeignKey(default=19, on_delete=django.db.models.deletion.CASCADE, related_name='teampages', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-12-13 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-media', '0015_livestreaming_event_location'),
        ('organization-network', '0108_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medias', to='organization-network.Department', verbose_name='department')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department', to='organization-media.Media', verbose_name='media')),
            ],
        ),
    ]

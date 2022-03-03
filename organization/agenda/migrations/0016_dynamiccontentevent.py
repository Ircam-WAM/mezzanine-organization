# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-04 17:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mezzanine_agenda', '0015_auto_20161021_1937'),
        ('organization_agenda', '0015_auto_20161026_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicContentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('object_id', models.PositiveIntegerField(editable=False, null=True, verbose_name='related object')),
                ('content_type', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dynamic_content_event', to='mezzanine_agenda.Event', verbose_name='event')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Dynamic Content Event',
            },
        ),
    ]

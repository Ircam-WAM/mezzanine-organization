# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-04 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_agenda', '0015_auto_20161021_1937'),
        ('organization_agenda', '0016_dynamiccontentevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRelatedTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1024, null=True, verbose_name='title')),
                ('event', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_title', to='mezzanine_agenda.Event', verbose_name='event')),
            ],
            options={
                'verbose_name': 'related title',
            },
        ),
        migrations.AlterOrderWithRespectTo(
            name='eventrelatedtitle',
            order_with_respect_to='event',
        ),
    ]

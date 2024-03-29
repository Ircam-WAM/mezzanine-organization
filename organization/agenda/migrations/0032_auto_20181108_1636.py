# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-08 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_agenda', '0028_auto_20180926_1235'),
        ('organization_network', '0114_auto_20181102_1151'),
        ('organization_agenda', '0031_auto_20181102_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPersonListBlockInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persons_list', to='mezzanine_agenda.Event', verbose_name='event')),
                ('person_list_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='organization_network.PersonListBlock', verbose_name='Person List Block')),
            ],
            options={
                'verbose_name': 'Person List',
            },
        ),
        migrations.RemoveField(
            model_name='eventperson',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventperson',
            name='person',
        ),
        migrations.DeleteModel(
            name='EventPerson',
        ),
    ]

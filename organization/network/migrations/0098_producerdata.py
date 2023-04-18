# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-04-07 08:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0097_auto_20170406_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProducerData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_description', models.CharField(help_text='Do you have prior experience with working in organizations in a co-creation process? If so, please describe it. (40 to 60 words)', max_length=60, verbose_name='experience description')),
                ('producer_description', models.TextField(help_text='**Description of the producer organization and the resources they bring for the proposal (100 to 150 words).', verbose_name='producer description')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='producer_data', to='organization_network.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name': 'Producer data',
                'verbose_name_plural': 'Producer data',
            },
        ),
    ]

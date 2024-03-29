# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-16 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0011_auto_20160916_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'activity function',
            },
        ),
        migrations.AddField(
            model_name='personactivity',
            name='function',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.ActivityFunction', verbose_name='function'),
        ),
    ]

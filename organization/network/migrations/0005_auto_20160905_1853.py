# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 16:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0004_organizationaudio_organizationblock_organizationimage_organizationlink_organizationvideo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UMR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'UMR',
            },
        ),
        migrations.RemoveField(
            model_name='person',
            name='permanent',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='function',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='rd_quota',
        ),
        migrations.AddField(
            model_name='personactivity',
            name='is_permanent',
            field=models.BooleanField(default=False, verbose_name='permanent'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='rd_quota_float',
            field=models.IntegerField(blank=True, null=True, verbose_name='R&D quota (float)'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='rd_quota_text',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='R&D quota (text)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='umr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.UMR', verbose_name='training type'),
        ),
    ]

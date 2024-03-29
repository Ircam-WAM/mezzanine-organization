# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-22 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0069_auto_20161216_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityWeeklyHourVolume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('monday_hours', models.IntegerField(verbose_name='monday hours')),
                ('tuesday_hours', models.IntegerField(verbose_name='tuesday hours')),
                ('wednesday_hours', models.IntegerField(verbose_name='wednesday hours')),
                ('thursday_hours', models.IntegerField(verbose_name='thursday hours')),
                ('friday_hours', models.IntegerField(verbose_name='friday hours')),
            ],
            options={
                'verbose_name_plural': 'Activity Weekly Hour Volumes',
                'verbose_name': 'Activity Weekly Hour Volume',
            },
        ),
        migrations.CreateModel(
            name='PersonActivityWeeklyHourVolume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday_hours', models.IntegerField(blank=True, null=True, verbose_name='monday hours')),
                ('tuesday_hours', models.IntegerField(blank=True, null=True, verbose_name='tuesday hours')),
                ('wednesday_hours', models.IntegerField(blank=True, null=True, verbose_name='wednesday hours')),
                ('thursday_hours', models.IntegerField(blank=True, null=True, verbose_name='thursday hours')),
                ('friday_hours', models.IntegerField(blank=True, null=True, verbose_name='friday hours')),
                ('activity', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_activity_weekly_hour_volume', to='organization_network.PersonActivity', verbose_name='activity')),
            ],
            options={
                'verbose_name': 'Person Activity Weekly Hour Volume',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='register_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='register ID'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='weekly_hour_volume',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.ActivityWeeklyHourVolume'),
        ),
    ]

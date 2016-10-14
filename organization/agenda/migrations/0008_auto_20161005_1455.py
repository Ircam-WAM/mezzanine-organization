# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-05 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_agenda', '0010_remove_event_language'),
        ('organization-agenda', '0007_auto_20160929_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateTimeField(blank=True, null=True, verbose_name='begin date')),
                ('date_to', models.DateTimeField(blank=True, null=True, verbose_name='end date')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='periods', to='mezzanine_agenda.Event', verbose_name='event')),
            ],
            options={
                'verbose_name_plural': 'periods',
                'verbose_name': 'period',
            },
        ),
        migrations.CreateModel(
            name='EventPublicType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('name_fr', models.CharField(max_length=512, null=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=512, null=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name_plural': 'public types',
                'verbose_name': 'public type',
            },
        ),
        migrations.CreateModel(
            name='EventTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('fr', 'French'), ('en', 'English')], max_length=64, null=True, verbose_name='Language')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings', to='mezzanine_agenda.Event', verbose_name='event')),
            ],
            options={
                'verbose_name_plural': 'trainings',
                'verbose_name': 'training',
            },
        ),
        migrations.CreateModel(
            name='EventTrainingLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('name_fr', models.CharField(max_length=512, null=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=512, null=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name_plural': 'training levels',
                'verbose_name': 'training level',
            },
        ),
        migrations.AddField(
            model_name='eventtraining',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings', to='organization-agenda.EventTrainingLevel', verbose_name='level'),
        ),
        migrations.AddField(
            model_name='eventtraining',
            name='public_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings', to='organization-agenda.EventPublicType', verbose_name='public type'),
        ),
    ]
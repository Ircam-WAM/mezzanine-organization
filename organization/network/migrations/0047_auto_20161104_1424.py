# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-04 13:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0046_auto_20161026_1025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personactivity',
            old_name='phd_postdoctoralsituation',
            new_name='phd_post_doctoral_situation',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='attachment_organization',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='phd_officers',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='second_employer',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='second_team',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='second_team_text',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='team',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='third_employer',
        ),
        migrations.AddField(
            model_name='personactivity',
            name='employers',
            field=models.ManyToManyField(blank=True, related_name='employer_project_activities', to='organization_network.Organization', verbose_name='employers'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_activities', to='organization_network.Organization', verbose_name='organization (attachment or subscribed)'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='supervisors',
            field=models.ManyToManyField(blank=True, related_name='supervisor_activities', to='organization_network.Person', verbose_name='supervisors'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='team_text',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='other team text'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='team_activities', to='organization_network.Team', verbose_name='teams'),
        ),
        migrations.AlterField(
            model_name='personactivity',
            name='rd_quota_float',
            field=models.FloatField(blank=True, null=True, verbose_name='R&D quota (float)'),
        ),
    ]

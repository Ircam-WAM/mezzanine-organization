# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 15:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization_projects', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
        ('organization_network', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='personactivity',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_projects.Project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='record_piece',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.RecordPiece'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='second_employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_employer_activity', to='organization_network.Organization', verbose_name='second employer'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='second_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_team_activity', to='organization_network.Team', verbose_name='second team'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.ActivityStatus', verbose_name='status'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_activity', to='organization_network.Team', verbose_name='team'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='training_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.TrainingLevel', verbose_name='training level'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='training_speciality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.TrainingSpectiality', verbose_name='training speciality'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='training_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.TrainingTopic', verbose_name='training topic'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='training_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.TrainingType', verbose_name='training type'),
        ),
        migrations.AddField(
            model_name='person',
            name='site',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='organization',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.OrganizationType', verbose_name='organization type'),
        ),
        migrations.AddField(
            model_name='departmentpage',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='organization_network.Department', verbose_name='department'),
        ),
        migrations.AddField(
            model_name='department',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='organization_network.Organization', verbose_name='organization'),
        ),
    ]

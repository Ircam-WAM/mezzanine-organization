# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-14 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0006_auto_20160914_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationaudio',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audios', to='organization_network.Organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='organizationblock',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blocks', to='organization_network.Organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='organizationimage',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='organization_network.Organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='organizationlink',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to='organization_network.Organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='organizationvideo',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='organization_network.Organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='personaudio',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audios', to='organization_network.Person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='personblock',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blocks', to='organization_network.Person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='personimage',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='organization_network.Person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to='organization_network.Person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='personvideo',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='organization_network.Person', verbose_name='person'),
        ),
    ]

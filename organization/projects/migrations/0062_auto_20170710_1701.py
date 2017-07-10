# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-07-10 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0106_personlistblockinline_site'),
        ('organization-projects', '0061_auto_20170706_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectResidencyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('file', mezzanine.core.fields.FileField(max_length=1024, verbose_name='Image')),
                ('credits', models.CharField(blank=True, max_length=256, null=True, verbose_name='credits')),
                ('type', models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured')], max_length=64, verbose_name='type')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='ProjectResidencyProducer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residencies', to='organization-network.Organization', verbose_name='producer')),
            ],
        ),
        migrations.RemoveField(
            model_name='projectresidency',
            name='producer',
        ),
        migrations.AddField(
            model_name='projectresidencyproducer',
            name='residency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='producers', to='organization-projects.ProjectResidency', verbose_name='residency'),
        ),
        migrations.AddField(
            model_name='projectresidencyimage',
            name='residency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='organization-projects.ProjectResidency', verbose_name='project residency image'),
        ),
    ]

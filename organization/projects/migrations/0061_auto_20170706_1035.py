# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-07-06 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0060_auto_20170421_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectResidencyUserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('file', models.FileField(max_length=1024, upload_to='user/images/%Y/%m/%d/', verbose_name='Image')),
                ('credits', models.CharField(blank=True, max_length=256, null=True, verbose_name='credits')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.AddField(
            model_name='projectresidency',
            name='address',
            field=models.TextField(blank=True, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='projectresidency',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='projectresidency',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='projectresidency',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=7, help_text='Calculated automatically if mappable location is set.', max_digits=10, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='projectresidency',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=7, help_text='Calculated automatically if mappable location is set.', max_digits=10, null=True, verbose_name='Longitude'),
        ),
        migrations.AddField(
            model_name='projectresidency',
            name='mappable_location',
            field=models.CharField(blank=True, help_text='This address will be used to calculate latitude and longitude. Leave blank and set Latitude and Longitude to specify the location yourself, or leave all three blank to auto-fill from the Location field.', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='projectresidency',
            name='postal_code',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='postal code'),
        ),
        migrations.AddField(
            model_name='projectresidencyuserimage',
            name='residency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_images', to='organization_projects.ProjectResidency', verbose_name='project residency user image'),
        ),
    ]

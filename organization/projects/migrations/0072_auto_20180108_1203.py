# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-01-08 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0071_auto_20171222_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='validation_status',
            field=models.IntegerField(choices=[(0, 'rejected'), (1, 'pending'), (2, 'in process'), (3, 'accepted'), (4, 'copied')], default=1, verbose_name='validation status'),
        ),
        migrations.AlterField(
            model_name='projectpublicdata',
            name='implementation_start_date',
            field=models.DateField(help_text='Possible period for the implementation of the residency (must be within the period of the project implementation workplan) (MM/DD/YYYY)', null=True, verbose_name='residency start date'),
        ),
    ]
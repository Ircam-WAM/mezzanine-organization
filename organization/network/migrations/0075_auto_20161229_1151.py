# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-29 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import organization.network.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0074_personactivitytimesheet_work_packages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityweeklyhourvolume',
            name='friday_hours',
        ),
        migrations.RemoveField(
            model_name='activityweeklyhourvolume',
            name='monday_hours',
        ),
        migrations.RemoveField(
            model_name='activityweeklyhourvolume',
            name='thursday_hours',
        ),
        migrations.RemoveField(
            model_name='activityweeklyhourvolume',
            name='tuesday_hours',
        ),
        migrations.RemoveField(
            model_name='activityweeklyhourvolume',
            name='wednesday_hours',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='friday_hours',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='monday_hours',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='thursday_hours',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='tuesday_hours',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='wednesday_hours',
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='friday_am',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='friday AM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='friday_pm',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='friday PM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='monday_am',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='monday AM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='monday_pm',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='monday PM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='thursday_am',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='thursday AM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='thursday_pm',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='thursday PM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='tuesday_am',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='tuesday AM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='tuesday_pm',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='tuesday PM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='wednesday_am',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='wednesday AM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityweeklyhourvolume',
            name='wednesday_pm',
            field=models.FloatField(default=0, validators=[organization.network.validators.validate_positive], verbose_name='wednesday PM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personactivity',
            name='friday_am',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='friday AM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='friday_pm',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='friday PM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='monday_am',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='monday AM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='monday_pm',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='monday PM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='thursday_am',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='thursday AM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='thursday_pm',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='thursday PM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='tuesday_am',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='tuesday AM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='tuesday_pm',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='tuesday PM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='wednesday_am',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='wednesday AM'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='wednesday_pm',
            field=models.FloatField(blank=True, null=True, validators=[organization.network.validators.validate_positive], verbose_name='wednesday PM'),
        ),
    ]

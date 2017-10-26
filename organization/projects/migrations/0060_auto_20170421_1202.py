# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-04-21 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0059_auto_20170418_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lead_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leader_projects', to='organization-network.Organization', verbose_name='lead organization'),
        ),
        migrations.AlterField(
            model_name='project',
            name='lead_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leader_projects', to='organization-network.Team', verbose_name='lead team'),
        ),
        migrations.AlterField(
            model_name='projectprivatedata',
            name='commitment_letter',
            field=models.FileField(help_text='Written on behalf of the whole project consortium, this letter will commit in implementing the collaboration of a residency application selected by the VERTIGO jury, on the conditions set by the project (in annex of letter: synthesis of all related information entered by project).<br>Please <a href="http://vertigo.starts.eu/media/uploads/vertigo%20starts/CALL/vertigo_loc_v3.rtf">download and use the template letter.</a>', max_length=1024, upload_to='user/documents/%Y/%m/%d/', verbose_name='letter of commitment by the project coordinator'),
        ),
        migrations.AlterField(
            model_name='projectpublicdata',
            name='implementation_duration',
            field=models.CharField(default='1', help_text='Possible duration of implementation in months (must be part of the project implementation workplan) (months)', max_length=128, verbose_name='residency duration'),
        ),
        migrations.AlterField(
            model_name='projectpublicdata',
            name='implementation_start_date',
            field=models.DateField(help_text='Possible start date of implementation (must be part of the project implementation workplan) (MM/DD/YYYY)', verbose_name='residency start date'),
        ),
    ]
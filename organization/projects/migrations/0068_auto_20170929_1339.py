# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-09-29 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0067_auto_20170922_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpublicdata',
            name='challenges_description',
            field=models.TextField(help_text='Description of the project technology to be made available to artist + challenges it produces (100 words - must include the elements to be made available to the artist with sufficient functional and implementation details for enabling him/her to elaborate a technical approach).', verbose_name='challenges description'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-21 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0017_auto_20160919_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagecustompersonlistblockinline',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_pages.CustomPage', verbose_name='Page'),
        ),
        migrations.AlterField(
            model_name='pagecustompersonlistblockinline',
            name='person_list_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization_network.PersonListBlock', verbose_name='Person List Block'),
        ),
        migrations.AlterField(
            model_name='personlistblockinline',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.Person', verbose_name='Person'),
        ),
        migrations.AlterField(
            model_name='personlistblockinline',
            name='person_list_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_network.PersonListBlock', verbose_name='Person List Block'),
        ),
    ]

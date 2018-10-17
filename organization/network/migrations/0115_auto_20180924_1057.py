# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-24 08:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0114_person_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityframework',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='activityframework',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='activityfunction',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='activityfunction',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='activitygrade',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='activitygrade',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='activitystatus',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='activitystatus',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='department',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='department',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='departmentpage',
            name='content_fr',
        ),
        migrations.RemoveField(
            model_name='departmentpage',
            name='sub_title_fr',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='bio_fr',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='opening_times_fr',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='subway_access_fr',
        ),
        migrations.RemoveField(
            model_name='organizationlink',
            name='title_fr',
        ),
        migrations.RemoveField(
            model_name='organizationrole',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='organizationrole',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='organizationservice',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='organizationservice',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='person',
            name='bio_fr',
        ),
        migrations.RemoveField(
            model_name='person',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='comments_fr',
        ),
        migrations.RemoveField(
            model_name='personblock',
            name='content_fr',
        ),
        migrations.RemoveField(
            model_name='personblock',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='personblock',
            name='title_fr',
        ),
        migrations.RemoveField(
            model_name='personlink',
            name='title_fr',
        ),
        migrations.RemoveField(
            model_name='personlistblock',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='personlistblock',
            name='title_fr',
        ),
        migrations.RemoveField(
            model_name='team',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='team',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='teamlink',
            name='title_fr',
        ),
        migrations.RemoveField(
            model_name='teampage',
            name='content_fr',
        ),
        migrations.RemoveField(
            model_name='teampage',
            name='sub_title_fr',
        ),
        migrations.RemoveField(
            model_name='traininglevel',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='traininglevel',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='trainingspeciality',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='trainingspeciality',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='trainingtopic',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='trainingtopic',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='trainingtype',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='trainingtype',
            name='name_fr',
        ),
    ]

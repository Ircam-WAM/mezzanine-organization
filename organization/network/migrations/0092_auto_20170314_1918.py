# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-14 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0091_auto_20170313_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationuserimage',
            name='file',
            field=models.FileField(max_length=1024, upload_to='user/images/%Y/%m/%d/', verbose_name='Image'),
        ),
    ]

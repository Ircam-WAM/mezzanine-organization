# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='value_en',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='value_fr',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]

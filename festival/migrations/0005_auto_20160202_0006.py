# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0004_auto_20160202_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='photo_credits',
            field=models.CharField(max_length=255, null=True, verbose_name='photo credits', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='artists',
            field=models.ManyToManyField(related_name='events', verbose_name='artists', to='festival.Artist', blank=True),
        ),
    ]

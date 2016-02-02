# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='artists',
            field=models.ManyToManyField(related_name='events', verbose_name='events', to='festival.Artist', blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='artists',
            field=models.ManyToManyField(related_name='videos', verbose_name='artists', to='festival.Artist', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0004_auto_20160229_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='photo_alignment',
            field=models.CharField(default=b'left', max_length=32, verbose_name='photo alignment', blank=True, choices=[(b'left', 'left'), (b'right', 'right')]),
        ),
    ]

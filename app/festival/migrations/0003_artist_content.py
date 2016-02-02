# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0002_auto_20160201_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='content',
            field=mezzanine.core.fields.RichTextField(default='', verbose_name='Content'),
            preserve_default=False,
        ),
    ]

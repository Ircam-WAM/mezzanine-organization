# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0002_auto_20141227_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='content_fr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='description_en',
            field=models.CharField(max_length=1000, null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='description_fr',
            field=models.CharField(max_length=1000, null=True, verbose_name='Description', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('festival', '0004_auto_20160225_0352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='name',
        ),
        migrations.AddField(
            model_name='artist',
            name='_meta_title',
            field=models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='content',
            field=mezzanine.core.fields.RichTextField(default='', verbose_name='Content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='artist',
            name='expiry_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='artist',
            name='in_sitemap',
            field=models.BooleanField(default=True, verbose_name='Show in sitemap'),
        ),
        migrations.AddField(
            model_name='artist',
            name='keywords_string',
            field=models.CharField(max_length=500, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='publish_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='short_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='site',
            field=models.ForeignKey(default=None, editable=False, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='slug',
            field=models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='status',
            field=models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')]),
        ),
        migrations.AddField(
            model_name='artist',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='artist',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='description_fr',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
    ]

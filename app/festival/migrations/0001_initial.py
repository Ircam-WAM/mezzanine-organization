# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_agenda', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('photo', models.ImageField(upload_to=b'images/%Y/%m/%d', max_length=1024, verbose_name='photo')),
                ('photo_credits', models.CharField(max_length=255, null=True, verbose_name='photo credits', blank=True)),
                ('bio', mezzanine.core.fields.RichTextField(null=True, verbose_name='bio', blank=True)),
            ],
            options={
                'db_table': 'festival_artists',
                'verbose_name': 'artist',
            },
        ),
        migrations.CreateModel(
            name='MetaEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eve_event_id', models.IntegerField(verbose_name='eve id', blank=True)),
                ('featured', models.BooleanField(verbose_name='featured')),
                ('featured_image', mezzanine.core.fields.FileField(max_length=1024, verbose_name='featured image', blank=True)),
                ('artists', models.ManyToManyField(related_name='metaevents', verbose_name='artists', to='festival.Artist', blank=True)),
                ('event', models.ForeignKey(related_name='meta_events', on_delete=django.db.models.deletion.SET_NULL, verbose_name='meta event', blank=True, to='mezzanine_agenda.Event', null=True)),
            ],
            options={
                'db_table': 'festival_meta_events',
                'verbose_name': 'meta event',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords_string', models.CharField(max_length=500, editable=False, blank=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('_meta_title', models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('status', models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True)),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True)),
                ('short_url', models.URLField(null=True, blank=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('media_id', models.IntegerField(verbose_name='media id')),
                ('event', models.ForeignKey(related_name='videos', on_delete=django.db.models.deletion.SET_NULL, verbose_name='meta event', blank=True, to='mezzanine_agenda.Event', null=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-05 22:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('ulysses_competitions', '0031_auto_20181025_1430'),
        ('organization-projects', '0076_merge_20181009_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords_string', models.CharField(blank=True, editable=False, max_length=500)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL')),
                ('_meta_title', models.CharField(blank=True, help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status')),
                ('publish_date', models.DateTimeField(blank=True, db_index=True, help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(blank=True, help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on')),
                ('short_url', models.URLField(blank=True, null=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('name', models.CharField(blank=True, max_length=512, verbose_name='name')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='end date')),
            ],
            options={
                'verbose_name': 'call',
                'verbose_name_plural': 'calls',
            },
        ),
        migrations.CreateModel(
            name='ProducerCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords_string', models.CharField(blank=True, editable=False, max_length=500)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL')),
                ('_meta_title', models.CharField(blank=True, help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status')),
                ('publish_date', models.DateTimeField(blank=True, db_index=True, help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(blank=True, help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on')),
                ('short_url', models.URLField(blank=True, null=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('name', models.CharField(blank=True, max_length=512, verbose_name='name')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name': 'producer call',
                'verbose_name_plural': 'producer calls',
            },
        ),
        migrations.AlterField(
            model_name='projectcallimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('header__responsive-logo-footer', 'responsive logo footer'), ('header__responsive-frame-video', 'responsive frame video')], max_length=64, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('header__responsive-logo-footer', 'responsive logo footer'), ('header__responsive-frame-video', 'responsive frame video')], max_length=64, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='projectresidencyimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('header__responsive-logo-footer', 'responsive logo footer'), ('header__responsive-frame-video', 'responsive frame video')], max_length=64, verbose_name='type'),
        ),
        migrations.AddField(
            model_name='call',
            name='producer_call',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calls', to='organization-projects.ProducerCall', verbose_name='producer call'),
        ),
        migrations.AddField(
            model_name='call',
            name='project_call',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calls', to='organization-projects.ProjectCall', verbose_name='project call'),
        ),
        migrations.AddField(
            model_name='call',
            name='residency_call',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calls', to='ulysses_competitions.Competition', verbose_name='residency call'),
        ),
        migrations.AddField(
            model_name='call',
            name='site',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
    ]
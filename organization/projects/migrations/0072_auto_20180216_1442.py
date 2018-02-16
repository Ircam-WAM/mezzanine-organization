# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-02-16 13:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('organization-projects', '0071_auto_20171222_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicCollectionProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('object_id', models.PositiveIntegerField(editable=False, null=True, verbose_name='related object')),
            ],
            options={
                'verbose_name': 'Dynamic Collection Project',
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='ProjectCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords_string', models.CharField(blank=True, editable=False, max_length=500)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('title_fr', models.CharField(max_length=500, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=500, null=True, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('_meta_title', models.CharField(blank=True, help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status')),
                ('publish_date', models.DateTimeField(blank=True, db_index=True, help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from')),
                ('expiry_date', models.DateTimeField(blank=True, help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on')),
                ('short_url', models.URLField(blank=True, null=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectCollectionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('file', mezzanine.core.fields.FileField(max_length=1024, verbose_name='Image')),
                ('credits', models.CharField(blank=True, max_length=256, null=True, verbose_name='credits')),
                ('type', models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured')], max_length=64, verbose_name='type')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='organization-projects.ProjectCollection', verbose_name='collection')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='ProjectCollectionProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='organization-projects.Project')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='organization-projects.ProjectCollection', verbose_name='collection')),
            ],
            options={
                'abstract': False,
            },
            bases=('organization-projects.project',),
        ),
        migrations.AddField(
            model_name='dynamiccollectionproject',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dynamic_collection_collection', to='organization-projects.ProjectCollection', verbose_name='collection'),
        ),
        migrations.AddField(
            model_name='dynamiccollectionproject',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AddField(
            model_name='dynamiccollectionproject',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_collection_project', to='organization-projects.Project', verbose_name='project'),
        ),
    ]

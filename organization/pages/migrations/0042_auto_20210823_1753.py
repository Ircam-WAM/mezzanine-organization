# Generated by Django 2.2.24 on 2021-08-23 15:53

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization-pages', '0041_auto_20190703_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontenthomebody',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamiccontenthomemedia',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamiccontenthomeslider',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamiccontentpage',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamicmultimediapage',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='homeimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='linkimage',
            name='image',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='pageimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='pagelink',
            name='link_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization-core.LinkType', verbose_name='link type'),
        ),
    ]
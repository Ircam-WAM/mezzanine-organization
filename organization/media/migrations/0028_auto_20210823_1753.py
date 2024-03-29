# Generated by Django 2.2.24 on 2021-08-23 15:53

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_media', '0027_media_iframe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='mediatranscoded',
            name='file',
            field=mezzanine.core.fields.FileField(blank=True, max_length=1024, null=True, upload_to='uploads/media/', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='mediatranscoded',
            name='media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transcoded', to='organization_media.Media', verbose_name='media'),
        ),
    ]

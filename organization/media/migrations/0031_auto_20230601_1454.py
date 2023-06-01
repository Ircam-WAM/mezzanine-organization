# Generated by Django 3.2.19 on 2023-06-01 12:54

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_media', '0030_merge_20230424_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaimage',
            name='file',
            field=mezzanine.core.fields.FileField(blank=True, max_length=1024, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='mediaimage',
            name='type',
            field=models.CharField(blank=True, choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_back', 'logo back'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('hero', 'hero'), ('banner', 'banner')], max_length=64, null=True, verbose_name='type'),
        ),
    ]

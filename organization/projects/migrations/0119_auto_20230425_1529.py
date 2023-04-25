# Generated by Django 3.2.18 on 2023-04-25 13:29

from django.db import migrations, models
from organization.core.fields import JSONField


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0118_merge_0116_auto_20230424_1520_0117_auto_20230424_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpageimage',
            name='crop_data',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='configuration',
            field=JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='projectpageimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('logo_header', 'logo header'), ('logo_back', 'logo back'), ('logo_footer', 'logo footer'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured'), ('hero', 'hero'), ('banner', 'banner')], max_length=64, verbose_name='type'),
        ),
    ]

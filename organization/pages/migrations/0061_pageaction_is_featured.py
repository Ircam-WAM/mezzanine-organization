# Generated by Django 3.2.19 on 2023-08-29 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0060_auto_20230829_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageaction',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='wether this topic is featured for external applications'),
        ),
    ]

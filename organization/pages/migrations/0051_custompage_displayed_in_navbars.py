# Generated by Django 3.2.8 on 2021-12-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0050_custompage_display_navbar'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompage',
            name='displayed_in_navbars',
            field=models.BooleanField(default=True),
        ),
    ]
# Generated by Django 3.2.18 on 2023-04-25 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_job', '0033_merge_0016_auto_20230424_1520_0032_auto_20230424_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobofferimage',
            name='crop_data',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
    ]

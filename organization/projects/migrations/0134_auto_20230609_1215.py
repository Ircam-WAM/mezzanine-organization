# Generated by Django 3.2.19 on 2023-06-09 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0133_merge_20230602_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttopic',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projecttopic',
            name='submitted_on',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
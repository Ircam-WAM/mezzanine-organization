# Generated by Django 3.2.19 on 2023-08-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0136_project_show_commits'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttopic',
            name='score',
            field=models.IntegerField(default=1, verbose_name='Score'),
        ),
    ]

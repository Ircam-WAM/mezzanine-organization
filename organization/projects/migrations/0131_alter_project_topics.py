# Generated by Django 3.2.19 on 2023-06-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0130_alter_project_meta_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='projects', to='organization_projects.ProjectTopic', verbose_name='topics'),
        ),
    ]

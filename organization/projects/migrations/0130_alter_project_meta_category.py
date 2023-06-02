# Generated by Django 3.2.19 on 2023-06-02 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_core', '0013_alter_metacategory_logo'),
        ('organization_projects', '0129_auto_20230601_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='meta_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='organization_core.metacategory', verbose_name='category'),
        ),
    ]
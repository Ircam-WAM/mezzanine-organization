# Generated by Django 2.2.24 on 2021-08-23 15:53

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0093_auto_20200728_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontentproject',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamiccontentprojectpage',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamicmultimediaproject',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='projectcallfile',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='documents', verbose_name='document'),
        ),
        migrations.AlterField(
            model_name='projectcallimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='projectcalllink',
            name='link_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_core.LinkType', verbose_name='link type'),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='documents', verbose_name='document'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='projectlink',
            name='link_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization_core.LinkType', verbose_name='link type'),
        ),
        migrations.AlterField(
            model_name='projectpage',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='organization_projects.Project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='projectpageimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='projectresidencyfile',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='documents', verbose_name='document'),
        ),
        migrations.AlterField(
            model_name='projectresidencyimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='projecttopic',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topics', to='organization_projects.ProjectTopic', verbose_name='parent topic'),
        ),
        migrations.AlterField(
            model_name='projectworkpackage',
            name='lead_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leader_work_packages', to='organization_network.Organization', verbose_name='lead organization'),
        ),
        migrations.AlterField(
            model_name='projectworkpackage',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='work_packages', to='organization_projects.Project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='system',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repositories', to='organization_projects.RepositorySystem', verbose_name='system'),
        ),
    ]
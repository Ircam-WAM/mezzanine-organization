# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 16:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('label', models.CharField(max_length=200, verbose_name='Label')),
                ('label_fr', models.CharField(max_length=200, null=True, verbose_name='Label')),
                ('label_en', models.CharField(max_length=200, null=True, verbose_name='Label')),
                ('field_type', models.IntegerField(choices=[(1, 'Single line text'), (2, 'Multi line text'), (3, 'Email'), (13, 'Number'), (14, 'URL'), (4, 'Check box'), (5, 'Check boxes'), (6, 'Drop down'), (7, 'Multi select'), (8, 'Radio buttons'), (9, 'File upload'), (10, 'Date'), (11, 'Date/time'), (15, 'Date of birth'), (12, 'Hidden')], verbose_name='Type')),
                ('required', models.BooleanField(default=True, verbose_name='Required')),
                ('visible', models.BooleanField(default=True, verbose_name='Visible')),
                ('choices', models.CharField(blank=True, help_text='Comma separated options where applicable. If an option itself contains commas, surround the option with `backticks`.', max_length=1000, verbose_name='Choices')),
                ('choices_fr', models.CharField(blank=True, help_text='Comma separated options where applicable. If an option itself contains commas, surround the option with `backticks`.', max_length=1000, null=True, verbose_name='Choices')),
                ('choices_en', models.CharField(blank=True, help_text='Comma separated options where applicable. If an option itself contains commas, surround the option with `backticks`.', max_length=1000, null=True, verbose_name='Choices')),
                ('default', models.CharField(blank=True, max_length=2000, verbose_name='Default value')),
                ('default_fr', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Default value')),
                ('default_en', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Default value')),
                ('placeholder_text', models.CharField(blank=True, max_length=100, verbose_name='Placeholder Text')),
                ('placeholder_text_fr', models.CharField(blank=True, max_length=100, null=True, verbose_name='Placeholder Text')),
                ('placeholder_text_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='Placeholder Text')),
                ('help_text', models.CharField(blank=True, max_length=100, verbose_name='Help text')),
                ('help_text_fr', models.CharField(blank=True, max_length=100, null=True, verbose_name='Help text')),
                ('help_text_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='Help text')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name_plural': 'Fields',
                'verbose_name': 'Field',
            },
        ),
        migrations.CreateModel(
            name='FieldEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_id', models.IntegerField()),
                ('value', models.CharField(max_length=2000, null=True)),
            ],
            options={
                'verbose_name': 'Form field entry',
                'verbose_name_plural': 'Form field entries',
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('content_fr', mezzanine.core.fields.RichTextField(null=True, verbose_name='Content')),
                ('content_en', mezzanine.core.fields.RichTextField(null=True, verbose_name='Content')),
                ('button_text', models.CharField(blank=True, max_length=50, verbose_name='Button text')),
                ('button_text_fr', models.CharField(blank=True, max_length=50, null=True, verbose_name='Button text')),
                ('button_text_en', models.CharField(blank=True, max_length=50, null=True, verbose_name='Button text')),
                ('response', mezzanine.core.fields.RichTextField(verbose_name='Response')),
                ('response_fr', mezzanine.core.fields.RichTextField(null=True, verbose_name='Response')),
                ('response_en', mezzanine.core.fields.RichTextField(null=True, verbose_name='Response')),
                ('send_email', models.BooleanField(default=True, help_text='To send an email to the email address supplied in the form upon submission, check this box.', verbose_name='Send email to user')),
                ('email_from', models.EmailField(blank=True, help_text='The address the email will be sent from', max_length=254, verbose_name='From address')),
                ('email_copies', models.CharField(blank=True, help_text='Provide a comma separated list of email addresses to be notified upon form submission. Leave blank to disable notifications.', max_length=200, verbose_name='Send email to others')),
                ('email_subject', models.CharField(blank=True, max_length=200, verbose_name='Subject')),
                ('email_subject_fr', models.CharField(blank=True, max_length=200, null=True, verbose_name='Subject')),
                ('email_subject_en', models.CharField(blank=True, max_length=200, null=True, verbose_name='Subject')),
                ('email_message', models.TextField(blank=True, help_text='Emails sent based on the above options will contain each of the form fields entered. You can also enter a message here that will be included in the email.', verbose_name='Message')),
                ('email_message_fr', models.TextField(blank=True, help_text='Emails sent based on the above options will contain each of the form fields entered. You can also enter a message here that will be included in the email.', null=True, verbose_name='Message')),
                ('email_message_en', models.TextField(blank=True, help_text='Emails sent based on the above options will contain each of the form fields entered. You can also enter a message here that will be included in the email.', null=True, verbose_name='Message')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name_plural': 'Forms',
                'verbose_name': 'Form',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='FormEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_time', models.DateTimeField(verbose_name='Date/time')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='forms.Form')),
            ],
            options={
                'verbose_name': 'Form entry',
                'verbose_name_plural': 'Form entries',
            },
        ),
        migrations.AddField(
            model_name='fieldentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='forms.FormEntry'),
        ),
        migrations.AddField(
            model_name='field',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='forms.Form'),
        ),
    ]
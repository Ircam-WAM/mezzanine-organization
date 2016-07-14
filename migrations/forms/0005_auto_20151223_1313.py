# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_auto_20150517_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='choices_en',
            field=models.CharField(help_text='Comma separated options where applicable. If an option itself contains commas, surround the option with `backticks`.', max_length=1000, null=True, verbose_name='Choices', blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='choices_fr',
            field=models.CharField(help_text='Comma separated options where applicable. If an option itself contains commas, surround the option with `backticks`.', max_length=1000, null=True, verbose_name='Choices', blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='default_en',
            field=models.CharField(max_length=2000, null=True, verbose_name='Default value', blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='default_fr',
            field=models.CharField(max_length=2000, null=True, verbose_name='Default value', blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='help_text_en',
            field=models.CharField(max_length=100, null=True, verbose_name='Help text', blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='help_text_fr',
            field=models.CharField(max_length=100, null=True, verbose_name='Help text', blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='label_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Label'),
        ),
        migrations.AddField(
            model_name='field',
            name='label_fr',
            field=models.CharField(max_length=200, null=True, verbose_name='Label'),
        ),
        migrations.AddField(
            model_name='field',
            name='placeholder_text_en',
            field=models.CharField(verbose_name='Placeholder Text', max_length=100, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='placeholder_text_fr',
            field=models.CharField(verbose_name='Placeholder Text', max_length=100, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='button_text_en',
            field=models.CharField(max_length=50, null=True, verbose_name='Button text', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='button_text_fr',
            field=models.CharField(max_length=50, null=True, verbose_name='Button text', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='form',
            name='content_fr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='form',
            name='email_message_en',
            field=models.TextField(help_text='Emails sent based on the above options will contain each of the form fields entered. You can also enter a message here that will be included in the email.', null=True, verbose_name='Message', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='email_message_fr',
            field=models.TextField(help_text='Emails sent based on the above options will contain each of the form fields entered. You can also enter a message here that will be included in the email.', null=True, verbose_name='Message', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='email_subject_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Subject', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='email_subject_fr',
            field=models.CharField(max_length=200, null=True, verbose_name='Subject', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='response_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Response'),
        ),
        migrations.AddField(
            model_name='form',
            name='response_fr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Response'),
        ),
    ]

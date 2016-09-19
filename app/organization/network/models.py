from __future__ import unicode_literals

import os
import re
import pwd
import time
import urllib
import string
import datetime
import mimetypes

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User

from mezzanine.pages.models import Page
from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from organization.core.models import *
from organization.media.models import *

from django_countries.fields import CountryField
# from .nationalities.fields import NationalityField

# Hack to have these strings translated
mr = _('Mr')
mrs = _('Ms')

GENDER_CHOICES = [
    ('male', _('male')),
    ('female', _('female')),
]

TITLE_CHOICES = [
    ('Dr', _('Dr')),
    ('Prof', _('Prof')),
    ('Prof Dr', _('Prof Dr')),
]

PATTERN_CHOICES = [
    ('pattern-bg--circles', _('circles')),
    ('pattern-bg--squares', _('squares')),
    ('pattern-bg--stripes', _('stripes')),
    ('pattern-bg--triangles', _('triangles')),
]

ALIGNMENT_CHOICES = (('left', _('left')), ('left', _('left')), ('right', _('right')))


class Address(models.Model):
    """(Address description)"""

    address = models.TextField(_('address'), blank=True)
    postal_code = models.CharField(_('postal code'), max_length=16, blank=True)
    country = CountryField(_('country'))

    def __str__(self):
        return ' '.join((self.address, self.postal_code))

    class Meta:
        abstract = True


class Organization(Named, Address, URL):
    """(Organization description)"""

    type = models.ForeignKey('OrganizationType', verbose_name=_('organization type'), blank=True, null=True, on_delete=models.SET_NULL)
    is_on_map = models.BooleanField(_('is on map'), default=True)

    class Meta:
        verbose_name = _('organization')


class OrganizationAudio(Audio):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='audios', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationVideo(Video):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='videos', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationLink(Link):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationImage(Image):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationBlock(Block):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationType(Named):
    """(OrganizationType description)"""

    class Meta:
        verbose_name = _('organization type')


class Department(Named):
    """(Department description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'), related_name="departments")

    class Meta:
        verbose_name = _('department')

    def __str__(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        return self.name


class DepartmentPage(Page, SubTitled, RichText):
    """(Department description)"""

    department = models.ForeignKey('Department', verbose_name=_('department'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)
    weaving_css_class = models.CharField(_('background pattern'), choices=PATTERN_CHOICES, max_length=64, blank=True)

    class Meta:
        verbose_name = _('department page')


class Team(Named, URL):
    """(Team description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'), related_name="teams", blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey('Department', verbose_name=_('department'), related_name="teams", blank=True, null=True, on_delete=models.SET_NULL)
    code = models.CharField(_('code'), max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = _('team')

    def __str__(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        elif self.department:
            if self.department.organization:
                return ' - '.join((self.department.organization.name, self.department.name, self.name))
            else:
                return ' - '.join((self.department.name, self.name))
        return self.name


class TeamPage(Page, SubTitled, RichText):
    """(Team description)"""

    team = models.ForeignKey('Team', verbose_name=_('team'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('team page')


class Person(Displayable, AdminThumbMixin):
    """(Person description)"""

    user = models.OneToOneField(User, verbose_name=_('user'), blank=True, null=True, on_delete=models.SET_NULL)
    person_title = models.CharField(_('title'), max_length=16, choices=TITLE_CHOICES, blank=True)
    gender = models.CharField(_('gender'), max_length=16, choices=GENDER_CHOICES, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    bio = RichTextField(_('biography'), blank=True)

    class Meta:
        verbose_name = _('person')
        ordering = ['last_name',]

    def __str__(self):
        return ' '.join((self.first_name, self.last_name))

    def get_absolute_url(self):
        return reverse("organization-network-person-detail", kwargs={'slug': self.slug})

    def set_names(self):
        names = self.title.split(' ')
        if len(names) == 1:
            self.first_name = ''
            self.last_name = names[0]
        elif len(names) == 2:
            self.first_name = names[0]
            self.last_name = names[1]
        else:
            self.first_name = names[0]
            self.last_name = ' '.join(names[1:])

    def clean(self):
        super(Person, self).clean()
        self.set_names()

    def save(self, *args, **kwargs):
        self.set_names()
        super(Person, self).save(*args, **kwargs)


class PersonAudio(Audio):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='audios', blank=True, null=True, on_delete=models.SET_NULL)


class PersonVideo(Video):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='videos', blank=True, null=True, on_delete=models.SET_NULL)


class PersonLink(Link):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class PersonImage(Image):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class PersonBlock(Block):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class PersonListBlock(Titled):

    page = models.ForeignKey(Page, verbose_name=_('Page'), related_name='person_list_block', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class PersonAutocomplete(models.Model):

    person_list_block = models.ForeignKey(PersonListBlock, verbose_name=_('Person List Block'), related_name='person_autocomplete', blank=True, null=True, on_delete=models.SET_NULL)
    person = models.ForeignKey(Person, verbose_name=_('Person'), related_name='person_list_block', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Person autocomplete')


class DynamicPersonList(DynamicContent, Orderable):

    person_list_block = models.ForeignKey("PersonListBlock", verbose_name=_('Person List Block'), related_name='dynamic_person_list', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Person List'


class ActivityStatus(Named):

    class Meta:
        verbose_name = _('activity status')


class ActivityGrade(Named):

    class Meta:
        verbose_name = _('activity grade')


class ActivityFramework(Named):

    class Meta:
        verbose_name = _('activity framework')


class ActivityFunction(Named):

    class Meta:
        verbose_name = _('activity function')


class BudgetCode(Named):

    class Meta:
        verbose_name = _('budget code')


class RecordPiece(Named):

    class Meta:
        verbose_name = _('record piece')


class TrainingType(Named):

    class Meta:
        verbose_name = _('training type')


class TrainingLevel(Named):

    class Meta:
        verbose_name = _('training level')


class TrainingTopic(Named):

    class Meta:
        verbose_name = _('training topic')


class TrainingSpectiality(Named):

    class Meta:
        verbose_name = _('training speciality')


class UMR(Named):

    class Meta:
        verbose_name = _('UMR')


class PersonActivity(Period):
    """(Activity description)"""

    person = models.ForeignKey('Person', verbose_name=_('person'))

    weeks = models.IntegerField(_('number of weeks'), blank=True, null=True)
    status = models.ForeignKey(ActivityStatus, verbose_name=_('status'), blank=True, null=True, on_delete=models.SET_NULL)
    is_permanent = models.BooleanField(_('permanent'), default=False)
    framework = models.ForeignKey(ActivityFramework, verbose_name=_('framework'), blank=True, null=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey(ActivityGrade, verbose_name=_('grade'), blank=True, null=True, on_delete=models.SET_NULL)
    function = models.ForeignKey(ActivityFunction, verbose_name=_('function'), blank=True, null=True, on_delete=models.SET_NULL)

    employer = models.ForeignKey(Organization, verbose_name=_('employer'), related_name='employer_activity', blank=True, null=True, on_delete=models.SET_NULL)
    attachment_organization = models.ForeignKey(Organization, verbose_name=_('attachment organization'), related_name='attachment_activity', blank=True, null=True, on_delete=models.SET_NULL)
    second_employer = models.ForeignKey(Organization, verbose_name=_('second employer'), related_name='second_employer_activity', blank=True, null=True, on_delete=models.SET_NULL)
    umr = models.ForeignKey(UMR, verbose_name=_('UMR'), blank=True, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey('Team', verbose_name=_('team'), related_name='team_activity', blank=True, null=True, on_delete=models.SET_NULL)
    second_team = models.ForeignKey('Team', verbose_name=_('second team'), related_name='second_team_activity', blank=True, null=True, on_delete=models.SET_NULL)

    project = models.ForeignKey('organization-projects.Project', verbose_name=_('project'), blank=True, null=True, on_delete=models.SET_NULL)
    rd_quota_float = models.IntegerField(_('R&D quota (float)'), blank=True, null=True)
    rd_quota_text = models.CharField(_('R&D quota (text)'), blank=True, null=True, max_length=128)
    rd_program = models.TextField(_('R&D program'), blank=True)
    budget_code = models.ForeignKey(BudgetCode, blank=True, null=True, on_delete=models.SET_NULL)

    phd_doctoral_school = models.ForeignKey(Organization, verbose_name=_('doctoral school'), blank=True, null=True, on_delete=models.SET_NULL)
    phd_director = models.ForeignKey('Person', verbose_name=_('PhD director'), related_name='phd_director_activity', blank=True, null=True, on_delete=models.SET_NULL)
    phd_officer_1 = models.ForeignKey('Person', verbose_name=_('PhD officer 1'), related_name='phd_officer_1_activity', blank=True, null=True, on_delete=models.SET_NULL)
    phd_officer_2 = models.ForeignKey('Person', verbose_name=_('PhD officer 2'), related_name='phd_officer_2_activity', blank=True, null=True, on_delete=models.SET_NULL)
    phd_defense_date = models.DateField(_('PhD defense date'), blank=True, null=True)
    phd_title = models.TextField(_('PhD title'), blank=True)
    phd_postdoctoralsituation =  models.CharField(_('post-doctoral situation'), blank=True, max_length=256)
    hdr = models.BooleanField(_('HDR'), default=False)

    training_type = models.ForeignKey(TrainingType, verbose_name=_('training type'), blank=True, null=True, on_delete=models.SET_NULL)
    training_level = models.ForeignKey(TrainingLevel, verbose_name=_('training level'), blank=True, null=True, on_delete=models.SET_NULL)
    training_topic = models.ForeignKey(TrainingTopic, verbose_name=_('training topic'), blank=True, null=True, on_delete=models.SET_NULL)
    training_speciality = models.ForeignKey(TrainingSpectiality, verbose_name=_('training speciality'), blank=True, null=True, on_delete=models.SET_NULL)
    training_title = models.TextField(_('Training title'), blank=True)

    record_piece = models.ForeignKey(RecordPiece, blank=True, null=True, on_delete=models.SET_NULL)

    date_added = models.DateTimeField(_('add date'), auto_now_add=True)
    date_modified = models.DateTimeField(_('modification date'), auto_now=True)
    date_modified_manual = models.DateTimeField(_('manual modification date'), blank=True, null=True)

    comments = models.TextField(_('comments'), blank=True)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')

    def __str__(self):
        if self.status:
            return ' - '.join((self.status.name, str(self.date_begin), str(self.date_end)))
        else:
            return ' - '.join((str(self.date_begin), str(self.date_end)))

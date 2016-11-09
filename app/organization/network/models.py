from __future__ import unicode_literals

import os
import re
import pwd
import time
import urllib
import string
import datetime
import mimetypes

from geopy.geocoders import GoogleV3 as GoogleMaps
from geopy.exc import GeocoderQueryError

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from mezzanine.pages.models import Page
from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from organization.core.models import *
from organization.media.models import *
from organization.pages.models import CustomPage

# from .nationalities.fields import NationalityField

# Hack to have these strings translated
mr = _('Mr')
mrs = _('Ms')

GENDER_CHOICES = [
    ('male', _('male')),
    ('female', _('female')),
]

PERSON_LIST_STYLE_CHOICES = [
    ('square', _('square')),
    ('circle', _('circle')),
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


class Organization(Named, Address, URL, AdminThumbRelatedMixin):
    """(Organization description)"""

    mappable_location = models.CharField(max_length=128, blank=True, null=True, help_text="This address will be used to calculate latitude and longitude. Leave blank and set Latitude and Longitude to specify the location yourself, or leave all three blank to auto-fill from the Location field.")
    lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Latitude", help_text="Calculated automatically if mappable location is set.")
    lon = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Longitude", help_text="Calculated automatically if mappable location is set.")
    type = models.ForeignKey('OrganizationType', verbose_name=_('organization type'), blank=True, null=True, on_delete=models.SET_NULL)
    initials = models.CharField(_('initials'), max_length=128, blank=True, null=True)
    is_on_map = models.BooleanField(_('is on map'), default=False, blank=True)
    is_host = models.BooleanField(_('is host'), default=False, blank=True)

    admin_thumb_type = 'logo'

    class Meta:
        verbose_name = _('organization')
        ordering = ['name',]

    def clean(self):
        """
        Validate set/validate mappable_location, longitude and latitude.
        """
        super(Organization, self).clean()

        if self.lat and not self.lon:
            raise ValidationError("Longitude required if specifying latitude.")

        if self.lon and not self.lat:
            raise ValidationError("Latitude required if specifying longitude.")

        if not (self.lat and self.lon) and not self.mappable_location:
            if self.address:
                self.mappable_location = self.address.replace("\n"," ").replace('\r', ' ') + ", " + self.postal_code + " " + self.city

        if self.mappable_location and not (self.lat and self.lon): #location should always override lat/long if set
            g = GoogleMaps(domain=settings.EVENT_GOOGLE_MAPS_DOMAIN)
            try:
                mappable_location, (lat, lon) = g.geocode(self.mappable_location)
            except GeocoderQueryError as e:
                raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
            except ValueError as e:
                raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
            except TypeError as e:
                raise ValidationError("The mappable location you specified could not be found. Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.")
            self.mappable_location = mappable_location
            self.lat = lat
            self.lon = lon

    def save(self):
        self.clean()
        super(Organization, self).save()


class OrganizationPlaylist(PlaylistRelated):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationLink(Link):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationImage(Image):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationBlock(Block):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationType(Named):
    """(OrganizationType description)"""

    css_class = models.CharField(_('class css'), max_length=64, blank=True, null=True,  help_text="Determine color on map.")

    class Meta:
        verbose_name = _('organization type')
        ordering = ['name',]


class Department(Named):
    """(Department description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'), related_name="departments")

    class Meta:
        verbose_name = _('department')
        ordering = ['name',]

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
    is_legacy = models.BooleanField(_('is legacy'), default=False)
    parent = models.ForeignKey('Team', verbose_name=_('parent team'), related_name="children", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('team')
        ordering = ['name',]

    def __str__(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        elif self.department:
            if self.department.organization:
                return ' - '.join((self.department.organization.name, self.department.name, self.name))
            else:
                return ' - '.join((self.department.name, self.name))
        return self.name

    @property
    def short(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        elif self.department:
            if self.department.organization:
                return ' - '.join((self.department.organization.name, self.name))
            else:
                return ' - '.join((self.department.name, self.name))
        return self.name


class TeamPage(Page, SubTitled, RichText):
    """(Team description)"""

    team = models.ForeignKey('Team', verbose_name=_('team'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('team page')


class TeamLink(Link):

    team = models.ForeignKey(Team, verbose_name=_('team'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


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
    external_id = models.CharField(_('external ID'), blank=True, null=True, max_length=128)

    class Meta:
        verbose_name = _('person')
        ordering = ['last_name',]

    def __str__(self):
        return self.title

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

    # def clean(self):
    #     super(Person, self).clean()
    #     self.set_names()
    #
    # def save(self, *args, **kwargs):
    #     self.set_names()
    #     super(Person, self).save(*args, **kwargs)


class PersonPlaylist(PlaylistRelated):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)


class PersonLink(Link):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class PersonImage(Image):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class PersonFile(File):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='files', blank=True, null=True, on_delete=models.SET_NULL)


class PersonBlock(Block):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class PageCustomPersonListBlockInline(Titled):

    page = models.ForeignKey(CustomPage, verbose_name=_('Page'), related_name='page_custom_person_list_block_inlines', blank=True, null=True, on_delete=models.SET_NULL)
    person_list_block = models.ForeignKey("PersonListBlock", related_name='page_custom_person_list_block_inlines', verbose_name=_('Person List Block'), blank=True, null=True)

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class PersonListBlock(Titled, Dated):

    style = models.CharField(_('style'), max_length=16, choices=PERSON_LIST_STYLE_CHOICES)

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class PersonListBlockInline(models.Model):

    person_list_block = models.ForeignKey(PersonListBlock, verbose_name=_('Person List Block'), related_name='person_list_block_inlines', blank=True, null=True, on_delete=models.SET_NULL)
    person = models.ForeignKey(Person, verbose_name=_('Person'), related_name='person_list_block_inlines', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Person autocomplete')


class ActivityStatus(Named):

    order = models.IntegerField(_('order number'), default=100)
    display = models.BooleanField(_('display on team page'), blank=True, default=True)
    display_text = models.CharField(_('display text'), max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = _('activity status')
        ordering = ['order']


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


class TrainingSpeciality(Named):

    class Meta:
        verbose_name = _('training speciality')


class UMR(Named):

    class Meta:
        verbose_name = _('UMR')


class PersonActivity(Period):
    """(Activity description)"""

    person = models.ForeignKey('Person', verbose_name=_('person'), related_name='activities')

    weeks = models.IntegerField(_('number of weeks'), blank=True, null=True)
    status = models.ForeignKey(ActivityStatus, verbose_name=_('status'), blank=True, null=True, related_name='activities', on_delete=models.SET_NULL)
    is_permanent = models.BooleanField(_('permanent'), default=False)
    framework = models.ForeignKey(ActivityFramework, verbose_name=_('framework'), blank=True, null=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey(ActivityGrade, verbose_name=_('grade'), blank=True, null=True, on_delete=models.SET_NULL)
    function = models.ForeignKey(ActivityFunction, verbose_name=_('function'), blank=True, null=True, on_delete=models.SET_NULL)

    organizations = models.ManyToManyField(Organization, verbose_name=_('organizations (attachment or subscribed)'), related_name='project_activities', blank=True)
    employers = models.ManyToManyField(Organization, verbose_name=_('employers'), related_name='employer_project_activities', blank=True)
    umr = models.ForeignKey(UMR, verbose_name=_('UMR'), blank=True, null=True, on_delete=models.SET_NULL)
    teams = models.ManyToManyField('Team', verbose_name=_('teams'), related_name='team_activities', blank=True)
    team_text = models.CharField(_('other team text'), blank=True, null=True, max_length=256)

    projects = models.ManyToManyField('organization-projects.Project', verbose_name=_('projects'), related_name='activities', blank=True)
    rd_quota_float = models.FloatField(_('R&D quota (float)'), blank=True, null=True)
    rd_quota_text = models.CharField(_('R&D quota (text)'), blank=True, null=True, max_length=128)
    rd_program = models.TextField(_('R&D program'), blank=True)
    budget_code = models.ForeignKey(BudgetCode, blank=True, null=True, on_delete=models.SET_NULL)

    supervisors = models.ManyToManyField('Person', verbose_name=_('supervisors'), related_name='supervisor_activities', blank=True)

    phd_doctoral_school = models.ForeignKey(Organization, verbose_name=_('doctoral school'), blank=True, null=True, on_delete=models.SET_NULL)
    phd_directors = models.ManyToManyField('Person', verbose_name=_('PhD directors'), related_name='phd_director_activities', blank=True)
    phd_defense_date = models.DateField(_('PhD defense date'), blank=True, null=True)
    phd_title = models.TextField(_('PhD title'), blank=True)
    phd_post_doctoral_situation =  models.CharField(_('post-doctoral situation'), blank=True, max_length=256)
    hdr = models.BooleanField(_('HDR'), default=False)

    training_type = models.ForeignKey(TrainingType, verbose_name=_('training type'), blank=True, null=True, on_delete=models.SET_NULL)
    training_level = models.ForeignKey(TrainingLevel, verbose_name=_('training level'), blank=True, null=True, on_delete=models.SET_NULL)
    training_topic = models.ForeignKey(TrainingTopic, verbose_name=_('training topic'), blank=True, null=True, on_delete=models.SET_NULL)
    training_speciality = models.ForeignKey(TrainingSpeciality, verbose_name=_('training speciality'), blank=True, null=True, on_delete=models.SET_NULL)
    training_title = models.TextField(_('Training title'), blank=True)

    record_piece = models.ForeignKey(RecordPiece, blank=True, null=True, on_delete=models.SET_NULL)

    date_added = models.DateTimeField(_('add date'), auto_now_add=True)
    date_modified = models.DateTimeField(_('modification date'), auto_now=True)
    date_modified_manual = models.DateTimeField(_('manual modification date'), blank=True, null=True)

    comments = models.TextField(_('comments'), blank=True)

    external_id = models.CharField(_('external ID'), blank=True, null=True, max_length=128)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['person__last_name',]

    def __str__(self):
        if self.status:
            return ' - '.join((self.status.name, str(self.date_from), str(self.date_to)))
        else:
            return ' - '.join((str(self.date_from), str(self.date_to)))

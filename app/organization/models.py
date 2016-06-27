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

from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to


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

ALIGNMENT_CHOICES = (('left', _('left')), ('right', _('right')))


class BaseNameModel(models.Model):
    """Base object with name and description"""

    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.__unicode__())


class Organization(BaseNameModel):
    """(Organization description)"""

    address = models.TextField(_('description'), blank=True)
    domain = models.CharField(_('domain'), max_length=255, blank=True)
    organization_type = models.ForeignKey('OrganizationType', verbose_name=_('organization type'), blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('organization')


class OrganizationType(models.Model):
    """(OrganizationType description)"""

    type = models.CharField(_('type'), max_length=255)

    def __unicode__(self):
        return self.type

    class Meta:
        verbose_name = _('organization type')


class Department(BaseNameModel):
    """(Department description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'))
    domain = models.CharField(_('domain'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('department')


class Team(BaseNameModel):
    """(Team description)"""

    department = models.ForeignKey('Department', verbose_name=_('department'), blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"Team"


class Person(Displayable, RichText, AdminThumbMixin):
    """(Person description)"""

    user = models.ForeignKey(User, verbose_name=_('user'), blank=True, null=True, on_delete=models.SET_NULL)
    person_title = models.CharField(_('Title'), max_length=16, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    organization = models.ForeignKey('Organization', verbose_name=_('organization'), blank=True, null=True, on_delete=models.SET_NULL)
    bio = RichTextField(_('biography'), blank=True)
    photo = FileField(_('photo'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_credits = models.CharField(_('photo credits'), max_length=255, blank=True, null=True)
    photo_alignment = models.CharField(_('photo alignment'), choices=ALIGNMENT_CHOICES, max_length=32, default="left", blank=True)
    photo_description = models.TextField(_('photo description'), blank=True)
    photo_featured = FileField(_('photo featured'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_featured_credits = models.CharField(_('photo featured credits'), max_length=255, blank=True, null=True)

    def __unicode__(self):
        return ' '.join((self.user.first_name, self.user.last_name))


class Link(models.Model):
    """A person can have many links."""

    person = models.ForeignKey('Person', verbose_name=_('Person'))
    link_type = models.ForeignKey('LinkType', verbose_name=_('Link type'))
    url = models.URLField(verbose_name=_('URL'))

    def __str__(self):
        return self.url


class LinkType(models.Model):
    """
    A link type could be ``Facebook`` or ``Twitter`` or ``Website``.
    This is masterdata that should be created by the admins when the site is
    deployed for the first time.
    :ordering: Enter numbers here if you want links to be displayed in a
      special order.
    """

    name=models.CharField(max_length=256, verbose_name=_('Name'))
    slug = models.SlugField(max_length=256, verbose_name=_('Slug'), help_text=_(
            'Use this field to define a simple identifier that can be used'
            ' to style the different link types (i.e. assign social media'
            ' icons to them)'),
        blank=True,
    )
    ordering = models.PositiveIntegerField(verbose_name=_('Ordering'), null=True, blank=True)

    class Meta:
        ordering = ['ordering', ]

    def __str__(self):
        return self.name


class Activity(models.Model):
    """(Activity description)"""

    person = models.ForeignKey('Person', verbose_name=_('person'))
    teams = models.ManyToManyField('Team', verbose_name=_('teams'))
    date_begin = models.DateField(_('begin date'), null=True, blank=True)
    date_end = models.DateField(_('end date'), null=True, blank=True)
    role = models.CharField(_('role'), blank=True, max_length=512)
    work = models.TextField(_('work'), blank=True)

    def __unicode__(self):
        return ' - '.join((self.person, self.role, self.date_begin, self.date_end))

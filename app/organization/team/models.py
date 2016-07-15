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

from django_countries.fields import CountryField

from organization.media.models import Photo
from organization.core.models import Named

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



class Address(models.Model):
    """(Address description)"""

    address = models.TextField(_('address'), blank=True)
    postal_code = models.CharField(_('postal code'), max_length=16, blank=True)
    country = CountryField(_('country'))

    def __unicode__(self):
        return u"Address"

        class Meta:
            abstract = True


class Organization(Named, Address):
    """(Organization description)"""

    type = models.ForeignKey('OrganizationType', verbose_name=_('organization type'), blank=True, null=True, on_delete=models.SET_NULL)
    url = models.URLField(_('URL'), max_length=512, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('organization')


class OrganizationType(Named):
    """(OrganizationType description)"""

    class Meta:
        verbose_name = _('organization type')


class Department(Named):
    """(Department description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'))
    url = models.URLField(_('URL'), max_length=512, blank=True)
    weaving_css_class = models.CharField(_('weaving CSS class'), max_length=64, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('department')


class Team(Named):
    """(Team description)"""

    department = models.ForeignKey('Department', verbose_name=_('department'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('team')

    def __unicode__(self):
        return self.name


class Person(AdminThumbMixin, Photo):
    """(Person description)"""

    user = models.ForeignKey(User, verbose_name=_('user'), blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('title'), max_length=16, choices=TITLE_CHOICES, blank=True)
    gender = models.CharField(_('gender'), max_length=16, choices=GENDER_CHOICES, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True)
    bio = RichTextField(_('biography'), blank=True)
    organization = models.ForeignKey('Organization', verbose_name=_('organization'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('person')
        ordering = ['last_name',]

    def __unicode__(self):
        return ' '.join((self.user.first_name, self.user.last_name))

    # def get_absolute_url(self):
    #     return reverse("festival-artist-detail", kwargs={'slug': self.slug})

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


class Nationality(models.Model):
    """(Nationality description)"""

    name = models.CharField(_('name'), max_length=128)

    class Meta:
        verbose_name = _('nationality')

    def __unicode__(self):
        return self.name


class Link(models.Model):
    """A person can have many links."""

    person = models.ForeignKey('Person', verbose_name=_('person'))
    link_type = models.ForeignKey('LinkType', verbose_name=_('link type'))
    url = models.URLField(verbose_name=_('URL'))

    class Meta:
        verbose_name = _('link')

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

    name = models.CharField(max_length=256, verbose_name=_('name'))
    slug = models.SlugField(max_length=256, verbose_name=_('slug'), help_text=_(
            'Use this field to define a simple identifier that can be used'
            ' to style the different link types (i.e. assign social media'
            ' icons to them)'),
        blank=True,
    )
    ordering = models.PositiveIntegerField(verbose_name=_('ordering'), null=True, blank=True)

    class Meta:
        ordering = ['ordering', ]

    def __str__(self):
        return self.name


class Activity(RichText):
    """(Activity description)"""

    person = models.ForeignKey('Person', verbose_name=_('person'))
    teams = models.ManyToManyField('Team', verbose_name=_('teams'))
    date_begin = models.DateField(_('begin date'), null=True, blank=True)
    date_end = models.DateField(_('end date'), null=True, blank=True)
    role = models.CharField(_('role'), blank=True, max_length=512)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('activity')

    def __unicode__(self):
        return ' - '.join((self.person, self.role, self.date_begin, self.date_end))

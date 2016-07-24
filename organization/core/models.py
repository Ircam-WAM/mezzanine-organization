from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.core.models import Displayable, Slugged


COLOR_CHOICES = (('black', _('black')), ('yellow', _('yellow')), ('red', _('red')))


class Description(models.Model):
    """Abstract model providing a description field"""

    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True


class Named(models.Model):
    """Abstract model providing a name field"""

    name = models.CharField(_('name'), max_length=512)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.__unicode__())


class Titled(models.Model):
    """Abstract model providing a title field"""

    title = models.CharField(_('name'), max_length=1024)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class SubTitle(models.Model):

    sub_title = models.TextField(_('sub title'), blank=True, max_length=1024)

    class Meta:
        abstract = True


class Category(Named):
    """Category description)"""

    class Meta:
        verbose_name = _('category')

    def __str__(self):
        return self.name


class BasicPage(Page, SubTitle, RichText):

    class Meta:
        verbose_name = 'basic page'


class PageBlock(Titled, RichText):

    background_color = models.CharField(_('background color'), max_length=32, choices=COLOR_CHOICES, blank=True)

    class Meta:
        verbose_name = 'page block'

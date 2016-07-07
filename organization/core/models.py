from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, OrderField, FileField


class Named(models.Model):
    """Named object with description"""

    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.__unicode__())


class Titled(models.Model):
    """Base object with title and description"""

    title = models.CharField(_('title'), max_length=512)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title


class SubTitle(models.Model):

    sub_title = models.TextField(_('sub title'), blank=True, max_length=1024)

    class Meta:
        abstract = True


class BasicPage(Page, RichText, SubTitle):

    class Meta:
        verbose_name = 'basic page'

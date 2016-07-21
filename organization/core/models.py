from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.core.models import Displayable, Slugged


class Description(models.Model):
    """Base object description"""

    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True


class Named(Description):
    """Named object with description"""

    name = models.CharField(_('name'), max_length=512)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.__unicode__())


class Titled(Slugged, Description):
    """Base object with title, slug and description"""

    class Meta:
        abstract = True


class SubTitle(models.Model):

    sub_title = models.TextField(_('sub title'), blank=True, max_length=1024)

    class Meta:
        abstract = True


class BasicPage(Page, RichText, SubTitle):

    class Meta:
        verbose_name = 'basic page'

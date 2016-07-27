from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.core.models import Displayable, Slugged, Orderable


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

    title = models.CharField(_('title'), max_length=1024)

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

    page = models.ForeignKey(Page, verbose_name=_('page'), blank=True, null=True, on_delete=models.SET_NULL)
    background_color = models.CharField(_('background color'), max_length=32, choices=COLOR_CHOICES, blank=True)

    class Meta:
        verbose_name = 'page block'


class PageImage(Orderable):
    """
    An image for a page
    """

    file = FileField(_("Image"), max_length=1024, format="Image", upload_to="images/pages")
    description = models.TextField(_('photo description'), blank=True)
    credits = models.CharField(_('photo credits'), max_length=256, blank=True, null=True)
    page = models.ForeignKey(Page)


    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        order_with_respect_to = "page"

    def __str__(self):
        value = self.description
        if not value:
            value = self.file.name
        if not value:
            value = ""
        return value

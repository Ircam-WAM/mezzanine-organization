from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.core.models import Displayable, Slugged, Orderable


COLOR_CHOICES = (('black', _('black')), ('yellow', _('yellow')), ('red', _('red')))
ALIGNMENT_CHOICES = (('left', _('left')), ('center', _('center')), ('right', _('right')))
IMAGE_TYPE_CHOICES = (('logo', _('logo')), ('slider', _('slider')), ('card', _('card')), ('content', _('content')))


class Description(models.Model):
    """Abstract model providing a description field"""

    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True


class Named(models.Model):
    """Abstract model providing a name field"""

    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True)

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
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class SubTitled(models.Model):

    sub_title = models.TextField(_('sub title'), blank=True, max_length=1024)

    class Meta:
        abstract = True


class Category(Named):
    """Category description)"""

    class Meta:
        verbose_name = _('category')

    def __str__(self):
        return self.name


class Block(RichText, Titled, Orderable):

    with_separator = models.BooleanField(default=False)
    background_color = models.CharField(_('background color'), max_length=32, choices=COLOR_CHOICES, blank=True)

    class Meta:
        abstract = True


class Image(Titled, Orderable):

    file = FileField(_("Image"), max_length=1024, format="Image", upload_to="images")
    credits = models.CharField(_('credits'), max_length=256, blank=True, null=True)
    type = models.CharField(_('type'), max_length=64, choices=IMAGE_TYPE_CHOICES, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        value = self.description
        if not value:
            value = self.file.name
        if not value:
            value = ""
        return value


class DynamicContent(models.Model):

    # used for autocomplete but hidden in admin
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content type'),
        null=True,
        blank=True,
        editable=False,
    )

    # used for autocomplete but hidden in admin
    object_id = models.PositiveIntegerField(
        verbose_name=_('related object'),
        null=True,
        editable=False,
    )

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class URL(models.Model):

    url = models.URLField(_('URL'), max_length=512, blank=True)

    class Meta:
        abstract = True


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


class Link(URL):
    """A person can have many links."""

    link_type = models.ForeignKey(LinkType, verbose_name=_('link type'))

    class Meta:
        abstract = True
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return self.url



class Period(models.Model):

    date_begin = models.DateField(_('begin date'), null=True, blank=True)
    date_end = models.DateField(_('end date'), null=True, blank=True)

    class Meta:
        abstract = True



class CustomDisplayable(Displayable):

    class Meta:
        verbose_name = _('custom displayable')


class DisplayableBlock(Block):

    displayable = models.ForeignKey(CustomDisplayable, verbose_name=_('displayable'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('block')
        verbose_name_plural = _("blocks")
        order_with_respect_to = "displayable"


class DisplayableImage(Image):

    displayable = models.ForeignKey(CustomDisplayable, verbose_name=_('displayable'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _("images")
        order_with_respect_to = "displayable"


class DisplayableLink(Link):

    displayable = models.ForeignKey(CustomDisplayable, verbose_name=_('displayable'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _("links")
        order_with_respect_to = "displayable"



class CustomModel(models.Model):

    class Meta:
        verbose_name = _('custom model')


class ModelBlock(Block):

    model = models.ForeignKey(CustomModel, verbose_name=_('model'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('block')
        verbose_name_plural = _("blocks")
        order_with_respect_to = "model"


class ModelImage(Image):

    model = models.ForeignKey(CustomModel, verbose_name=_('model'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _("images")
        order_with_respect_to = "model"


class ModelLink(Link):

    model = models.ForeignKey(CustomModel, verbose_name=_('model'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _("links")
        order_with_respect_to = "model"

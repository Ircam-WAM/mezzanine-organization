from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
#from orderable.models import Orderable
from organization.core.models import Named, Description, Image, Photo


class ArticleImage(Image):

    article_fk = models.ForeignKey("Article", verbose_name=_('article'))

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "article"

class Article(BlogPost, Photo):

    sub_title = models.CharField(_('sub title'), blank=True, max_length=1000)
    related_articles = models.ManyToManyField("self",
                                 verbose_name=_("Related articles"), blank=True)

    model_name = _('article')

    def get_absolute_url(self):
        return reverse("magazine-article-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('article')


class Brief(Displayable, RichText): #Orderable

    text_button = models.CharField(blank=True, max_length=150, null=False, verbose_name='text button')
    external_content = models.URLField(blank=True, max_length=1000, null=False, verbose_name='external content')

    # used for autocomplete but hidden in admin
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content page'),
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

    def get_absolute_url(self):
        return self.external_content

    class Meta:
        verbose_name = _('brief')
        #ordering = ['sort_order']


class Topic(Page, RichText):
    """Topic for magazine menu"""

    articles = models.ManyToManyField(Article, verbose_name=_('articles'), blank=True)

    class Meta:
        verbose_name = _('topic')

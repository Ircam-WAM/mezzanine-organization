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
from organization.network.models import Department, PersonListBlock
from organization.media.models import Audio, Video
from organization.core.models import *


class Article(BlogPost, SubTitled):

    department = models.ForeignKey(Department, verbose_name=_('department'), related_name='articles', limit_choices_to=dict(id__in=Department.objects.all()), blank=True, null=True, on_delete=models.SET_NULL)
    topics = models.ManyToManyField("Topic", verbose_name=_('topics'), related_name="articles", blank=True)

    def get_absolute_url(self):
        return reverse("magazine-article-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('article')


class ArticleImage(Image):

    article = models.ForeignKey("Article", verbose_name=_('article'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "article"


class ArticleAudio(Audio):

    article = models.ForeignKey(Article, verbose_name=_('article'), related_name='audios', blank=True, null=True, on_delete=models.SET_NULL)


class ArticleVideo(Video):

    article = models.ForeignKey(Article, verbose_name=_('article'), related_name='videos', blank=True, null=True, on_delete=models.SET_NULL)


class Brief(Displayable, RichText): #Orderable

    text_button = models.CharField(blank=True, max_length=150, null=False, verbose_name=_('text button'))
    external_content = models.URLField(blank=True, max_length=1000, null=False, verbose_name=_('external content'))

    # used for autocomplete but hidden in admin
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('local content'),
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

    class Meta:
        verbose_name = _('topic')


class ArticlePersonListBlockInline(Titled):

    article = models.ForeignKey(Article, verbose_name=_('Article'), related_name='article_person_list_block_inlines', blank=True, null=True, on_delete=models.SET_NULL)
    person_list_block = models.ForeignKey(PersonListBlock, related_name='article_person_list_block_inlines', verbose_name=_('Person List Block'), blank=True, null=True)

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class DynamicContentArticle(DynamicContent, Orderable):

    article = models.ForeignKey(Article, verbose_name=_('article'), related_name='dynamic_content_articles', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Article'

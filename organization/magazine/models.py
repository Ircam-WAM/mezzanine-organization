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
# from autocomplete.dal_queryset_sequence.fields import (
#         QuerySetSequenceModelField,
#         QuerySetSequenceModelMultipleField,
#     )
from organization.core.models import Named, Description, Image
from organization.media.models import Photo

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
    local_content = models.URLField(blank=False, max_length=1000, null=False, verbose_name='local content')

    limit = models.Q(app_label='organization-magazine', model='article') | \
        models.Q(app_label='organization-magazine', model='topic')
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content page'),
        limit_choices_to=limit,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('related object'),
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')


    def get_absolute_url(self):
        return self.local_content

    class Meta:
        verbose_name = _('brief')
        #ordering = ['sort_order']



# class BriefForm(forms.ModelForm):
#
#     selected_object = forms.ModelChoiceField(
#         queryset=ContentType.objects.all(),
#         widget=autocomplete.ModelSelect2(url='object-autocomplete')
#     )
#
#     class Meta:
#         model = Brief
#         fields = ('__all__')


class Topic(Page, RichText):
    """Topic for magazine menu"""

    articles = models.ManyToManyField(Article, verbose_name=_('articles'), blank=True)

    class Meta:
        verbose_name = _('topic')

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
#from mezzanine.core.models import Displayable
from mezzanine.pages.models import Page, RichText
# Create your models here.
# class DisplayableCustom(Displayable):
#
#     sub_title = models.TextField(_('sub_title'), blank=True)


class SubTitle(models.Model):

    sub_title = models.TextField(_('sub title'), blank=True)

    class Meta:
        abstract = True


class BasicPage(Page, RichText):

    sub_title = models.TextField(_('sub title'), blank=True)

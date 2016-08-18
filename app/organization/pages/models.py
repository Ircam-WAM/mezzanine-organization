from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from mezzanine.core.models import Displayable, Slugged, Orderable
from organization.core.models import DynamicContent


class DynamicContentHomeSlider(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Home Slider'

class DynamicContentHomeBody(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Home Body'

class Home(Displayable):

    class Meta:
        verbose_name = 'Home'

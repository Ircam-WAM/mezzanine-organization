from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from mezzanine.core.models import Displayable, Slugged, Orderable
from organization.core.models import *
from organization.media.models import *


class CustomPage(Page, SubTitled, RichText):

    class Meta:
        verbose_name = 'custom page'


class PageBlock(Block):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("block")
        verbose_name_plural = _("blocks")
        verbose_name = 'page block'


class PageImage(Image):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "page"


class PageAudio(Audio):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='audios', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("audio")
        verbose_name_plural = _("audios")
        order_with_respect_to = "page"


class PageVideo(Video):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='videos', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")
        order_with_respect_to = "page"


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
        verbose_name = _('home')
        verbose_name_plural = _("homes")

    def get_absolute_url(self):
        return reverse("organization-home")


class JobResponse(models.Model):

    first_name = models.CharField(max_length=255, null=False, verbose_name=_('first name'))
    last_name = models.CharField(max_length=255, null=False, verbose_name=_('last name'))
    email = models.EmailField(max_length=255, null=False, verbose_name=_('email'))
    #@TODO validate type format
    curriculum_vitae = FileField(_("curriculum_vitae"), max_length=1024, upload_to="job_responses/%Y/%m/%d/")
    cover_letter = FileField(_("curriculum_vitae"), max_length=1024, upload_to="job_responses/%Y/%m/%d/")
    job_offer = models.ForeignKey("JobOffer", verbose_name=_('job offer'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('job_reponse')
        verbose_name_plural = _("job_reponses")


class JobOffer(Displayable, RichText):

    email = models.EmailField(max_length=255, null=False, verbose_name=_('Email to forward response'))
    type = models.CharField(blank=True, choices=[('internship', 'internship'), ('job', 'job')], max_length=32, verbose_name='Job offer type')

    class Meta:
        verbose_name = _('job offer')
        verbose_name_plural = _("job offers")

    def get_absolute_url(self):
        return reverse("organization-job-offer-detail")

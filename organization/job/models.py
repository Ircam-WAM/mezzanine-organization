from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from mezzanine.core.models import Displayable
from organization.core.models import *
from organization.media.models import *

class JobResponse(models.Model):

    first_name = models.CharField(max_length=255, null=False, verbose_name=_('first name'))
    last_name = models.CharField(max_length=255, null=False, verbose_name=_('last name'))
    email = models.EmailField(max_length=255, null=False, verbose_name=_('email'))
    message = models.TextField(max_length=800, verbose_name=_('message'))
    #@TODO validate type format
    curriculum_vitae = models.FileField(_("curriculum vitae"), max_length=1024, upload_to="job_responses/%Y/%m/%d/")
    cover_letter = models.FileField(_("cover letter"), max_length=1024, upload_to="job_responses/%Y/%m/%d/")
    job_offer = models.ForeignKey("JobOffer", verbose_name=_('job offer'), related_name='job_response', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('job_reponse')
        verbose_name_plural = _("job_reponses")


class JobOffer(Displayable, RichText):

    email = models.EmailField(max_length=255, null=False, verbose_name=_('Email to forward response'))
    type = models.CharField(blank=True, choices=[('internship', 'internship'), ('job', 'job')], max_length=32, verbose_name='Job offer type')

    def get_absolute_url(self):
        return reverse("organization-job-offer-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('job offer')
        verbose_name_plural = _("job offers")


class Candidacy(Displayable, RichText, Period):

    text_button_external = models.CharField(blank=True, max_length=150, null=False, verbose_name=_('external text button'))
    text_button_internal = models.CharField(blank=True, max_length=150, null=False, verbose_name=_('internal text button'))
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
        verbose_name = _('candidacy')
        verbose_name_plural = _("candidacies")


class CandidacyImage(Image):

    candidacy = models.ForeignKey(Candidacy, verbose_name=_('candidacy'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

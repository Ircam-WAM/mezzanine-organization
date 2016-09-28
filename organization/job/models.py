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

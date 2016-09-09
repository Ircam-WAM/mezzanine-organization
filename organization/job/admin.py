from django.contrib import admin
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from organization.job.models import JobOffer


class JobOfferAdminDisplayable(BaseTranslationModelAdmin):

    model = JobOffer


admin.site.register(JobOffer, JobOfferAdminDisplayable)

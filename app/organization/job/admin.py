from django.contrib import admin
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from organization.job.models import JobOffer, JobResponse


class JobResponseInline(TabularDynamicInlineAdmin):

    model = JobResponse


class JobOfferAdminDisplayable(BaseTranslationModelAdmin):

    model = JobOffer
    inlines = [JobResponseInline,]


admin.site.register(JobOffer, JobOfferAdminDisplayable)

from django.contrib import admin
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from organization.job.models import *
from organization.job.forms import *


class JobResponseInline(TabularDynamicInlineAdmin):

    model = JobResponse


class JobOfferAdminDisplayable(BaseTranslationModelAdmin):

    model = JobOffer
    inlines = [JobResponseInline,]


class CandidacyImageInline(TabularDynamicInlineAdmin):

    model = CandidacyImage


class CandidacyAdmin(admin.ModelAdmin):

    model = Candidacy


class CandidacyAdminDisplayable(BaseTranslationModelAdmin,):

    list_display = ('title', 'external_content', 'content_object', )
    form = CandidacyForm
    inlines = [CandidacyImageInline,]
    exclude = ("short_url", "keywords", "description", "slug", )
    fieldsets = (
        (None, {
            'fields': ('title', 'status', 'publish_date', 'expiry_date', 'content', 'date_from', 'date_to', 'text_button_external', 'external_content', 'text_button_internal', 'content_object',),
        }),
    )


admin.site.register(JobOffer, JobOfferAdminDisplayable)
admin.site.register(Candidacy, CandidacyAdminDisplayable)

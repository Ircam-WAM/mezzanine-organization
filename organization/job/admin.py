# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin, TeamOwnableAdmin,\
    BaseTranslationModelAdmin
from organization.job.models import JobResponse, JobOfferImage, JobOffer,\
    CandidacyImage, Candidacy


class JobResponseInline(TabularDynamicInlineAdmin):

    model = JobResponse


class JobOfferImageInline(TabularDynamicInlineAdmin):

    model = JobOfferImage


class JobOfferAdminDisplayable(TeamOwnableAdmin, BaseTranslationModelAdmin):

    model = JobOffer
    inlines = [JobOfferImageInline, JobResponseInline, ]
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'status',
                'publish_date',
                'expiry_date',
                'description',
                'gen_description',
                'content',
                'email',
                'type',
                'text_button',
                'url',
            ),
        }),
    )


class JobResponseAdmin(TeamOwnableAdmin, BaseTranslationModelAdmin):

    model = JobResponse
    search_fields = ['last_name', 'first_name']
    list_display = ['first_name', 'last_name', 'email', 'job_offer']


class CandidacyImageInline(TabularDynamicInlineAdmin):

    model = CandidacyImage


class CandidacyAdminDisplayable(BaseTranslationModelAdmin,):

    model = Candidacy
    list_display = ('title', 'url', )
    inlines = [CandidacyImageInline, ]
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'status',
                'publish_date',
                'expiry_date',
                'description',
                'gen_description',
                'content',
                'date_from',
                'date_to',
                'text_button',
                'url',
            ),
        }),
    )


admin.site.register(JobResponse, JobResponseAdmin)
admin.site.register(JobOffer, JobOfferAdminDisplayable)
admin.site.register(Candidacy, CandidacyAdminDisplayable)

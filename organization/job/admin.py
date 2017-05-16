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
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from organization.job.models import *
from organization.job.forms import *
from organization.job.translation import *


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

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

from modeltranslation.translator import register, TranslationOptions
from organization.job.models import JobOffer, JobResponse, JobOfferImage,\
    Candidacy, CandidacyImage


@register(JobOffer)
class JobOfferTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content', 'text_button', )


@register(JobResponse)
class JobResponseTranslationOptions1(TranslationOptions):
    pass


@register(JobOfferImage)
class JobResponseTranslationOptions2(TranslationOptions):
    pass


@register(Candidacy)
class JobResponseTranslationOptions3(TranslationOptions):

    fields = ('title', 'description', 'content', 'text_button', )


@register(CandidacyImage)
class JobResponseTranslationOptions4(TranslationOptions):
    pass

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

from __future__ import unicode_literals

import django.views.i18n
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import permission_required
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.projects.views import *

urlpatterns = [
    url("^dynamic-content-project/$",  permission_required('organization-projects.change_project')(DynamicContentProjectView.as_view()), name='dynamic-content-project'),

    url("^projects/detail/(?P<slug>.*)/$", RedirectView.as_view(pattern_name = 'organization-project-projectpage-detail'), name='organization-project-detail'),
    url("^projects/pages/(?P<slug>.*)/$", ProjectPageView.as_view(), name='organization-project-projectpage-detail'),
    url("^projects/list/$", ProjectListView.as_view(), name='organization-project-list'),
    url("^projects/archives/list/$", ProjectArchivesListView.as_view(), name='organization-project-archive-list'),

    url("^team/(?P<slug>.*)/projects/list/$", ProjectTeamListView.as_view(), name='organization-project-team-list'),
    url("^team/(?P<slug>.*)/projects/archives/list/$", ProjectArchivesTeamListView.as_view(), name='organization-project-archive-team-list'),

    url("^projects/demo/(?P<slug>.*)/$", ProjectDemoDetailView.as_view(), name='organization-project-demo-detail'),
    url("^projects/blog/(?P<slug>.*)/$", ProjectBlogPageView.as_view(), name='organization-project-blogpage-detail'),

    # due to this commit 73743f67f1d1574dbeff6cc22aae37986d257a92, redirect to old patterns 'project' without 's'
    url("^project/detail/(?P<slug>.*)/$", RedirectView.as_view(pattern_name = 'organization-project-detail'), name="redirect-project-detail"),
    url("^project/demo/(?P<slug>.*)/$", RedirectView.as_view(pattern_name = 'organization-project-demo-detail'), name="redirect-project-demo"),
    url("^project/blog/(?P<slug>.*)/$", RedirectView.as_view(pattern_name = 'organization-project-blogpage-detail'), name="redirect-project-blog"),

    url("^ict-projects/list/$", ProjectICTListView.as_view(), name='organization-ict-project-list'),
    url("^ict-projects/(?P<slug>.*)/detail/$", ProjectICTDetailView.as_view(), name='organization-ict-project-detail'),

    url("^calls/(?P<slug>.*)/projects/create/public/$", ProjectICTCreatePublicFundingView.as_view(), name='organization-project-public-create'),
    url("^calls/(?P<slug>.*)/projects/create/private/$", ProjectICTCreatePrivateFundingView.as_view(), name='organization-project-private-create'),
    url("^calls/(?P<slug>.*)/projects/validation/$", ProjectICTValidationView.as_view(), name='organization-project-validation'),

    url("^calls/(?P<call_slug>.*)/projects/detail/(?P<slug>.*)/$", ProjectICTDetailView.as_view(), name='organization-project-detail'),
    url("^calls/(?P<call_slug>.*)/projects/list/$", ProjectICTListView.as_view(), name='organization-project-list'),

    url("^calls/(?P<slug>.*)/residencies/submission/$", ProjectResidencyCreateView.as_view(), name='organization-residency-create'),
    url("^calls/(?P<call_slug>.*)/residencies/(?P<slug>.*)/detail/$", ProjectResidencyDetailView.as_view(), name='organization-residency-detail'),
    url("^calls/(?P<call_slug>.*)/residencies/list/$", ProjectResidencyListView.as_view(), name='organization-residency-list'),

    url("^calls/$", ProjectCallListAsEventsView.as_view(), name='organization-call-list-as-events'),

    url("^calls/list/$", ProjectCallListView.as_view(), name='organization-call-list'),
    url("^calls/(?P<slug>.*)/detail/$", ProjectCallDetailView.as_view(), name='organization-call-detail'),

    url("^calls/(?P<slug>.*)/detail/projects/submission/$", ProjectCallDetailView.as_view(), name='organization-project-submission-hack1'), #HACK
    url("^calls/detail/(?P<slug>.*)/projects/submission/$", ProjectCallDetailView.as_view(), name='organization-project-submission-hack2'), #HACK

    url("^profile/project/(?P<slug>.*)/$", ProjectICTEditPublicFundingView.as_view(), name="user-project-edit"),
    url("^profile/project/private/(?P<slug>.*)/$", ProjectICTEditPrivateFundingView.as_view(), name="user-project-edit-private"),

]

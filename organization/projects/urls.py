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
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import permission_required
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.projects.views import *

urlpatterns = [
    url("^dynamic-content-project/$",  permission_required('project.can_edit')(DynamicContentProjectView.as_view()), name='dynamic-content-project'),

    # Old URLs
    url("^ict-projects/list/$", ProjectTechListView.as_view(), name='organization-ict-project-list'),
    url("^ict-projects/(?P<slug>.*)/detail/$", ProjectTechDetailView.as_view(), name='organization-ict-project-detail'),
    # due to this commit 73743f67f1d1574dbeff6cc22aae37986d257a92, redirect to old patterns 'project' without 's'
    url("^project/detail/(?P<slug>.*)/$", RedirectView.as_view(pattern_name = 'organization-project-detail'), name="redirect-project-detail"),
    url("^project/demo/(?P<slug>.*)/$", RedirectView.as_view(pattern_name = 'organization-project-demo-detail'), name="redirect-project-demo"),
    url("^project/blog/(?P<slug>.*)/$", RedirectView.as_view(pattern_name = 'organization-project-blogpage-detail'), name="redirect-project-blog"),
    
    # Projects
    url("^projects/$", ProjectListView.as_view(), name='organization-project-list'),
    url("^projects/(?P<slug>.*)/detail/$", ProjectDetailView.as_view(), name='organization-project-detail'),
    url("^projects/(?P<slug>.*)/demo/$", ProjectDemoDetailView.as_view(), name='organization-project-demo-detail'),
    url("^projects/(?P<slug>.*)/blog/$", ProjectBlogPageView.as_view(), name='organization-project-blogpage-detail'),

    # Call projects
    url("^calls/(?P<call_slug>.*)/projects/$", ProjectTechListView.as_view(), name='organization-call-project-list'),
    url("^calls/(?P<call_slug>.*)/projects/(?P<slug>.*)/detail/$", ProjectTechDetailView.as_view(), name='organization-call-project-detail'),
    url("^calls/(?P<call_slug>.*)/projects/(?P<funding>.*)/create/$", ProjectTechCreateView.as_view(), name='organization-call-project-create'),
    url("^calls/(?P<call_slug>.*)/projects/(?P<slug>.*)/update/$", ProjectTechUpdateView.as_view(), name="organization-call-project-update"),
    url("^calls/(?P<call_slug>.*)/projects/(?P<slug>.*)/validate/$", ProjectTechValidateView.as_view(), name='organization-call-project-validate'),

    # Call Residencies
    url("^calls/(?P<call_slug>.*)/residencies/$", ProjectResidencyListView.as_view(), name='organization-call-residency-list'),
    url("^calls/(?P<call_slug>.*)/residencies/submission/$", ProjectResidencyCreateView.as_view(), name='organization-residency-create'),
    url("^calls/(?P<call_slug>.*)/residencies/(?P<slug>.*)/detail/$", ProjectResidencyDetailView.as_view(), name='organization-residency-detail'),
    url("^calls/residencies/$", ProjectResidencyListView.as_view(), name='organization-all-residency-list'),

    # Calls
    url("^calls/$", ProjectCallListView.as_view(), name='organization-call-list'),
    url("^calls/as_events/$", ProjectCallListAsEventsView.as_view(), name='organization-call-list-as-events'),
    url("^calls/(?P<slug>.*)/detail/$", ProjectCallDetailView.as_view(), name='organization-call-detail'),

]

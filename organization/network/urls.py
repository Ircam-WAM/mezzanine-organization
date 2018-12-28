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

from organization.network.views import *


urlpatterns = [
    url('^directory(?:/(?P<letter>.*))?/$', PersonDirectoryView.as_view(letter="a"), name='person-directory'),
    url('^person/timesheet/declare-curr-month$', TimeSheetCreateCurrMonthView.as_view(), name='organization-network-timesheet-create-curr-month-view'),
    url('^person/timesheet/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/create/$', TimeSheetCreateView.as_view(), name='organization-network-timesheet-create-view'),
    url('^person/timesheet/$', PersonActivityTimeSheetListView.as_view(), name='organization-network-timesheet-list-view' ),
    url('^person(?:/(?P<slug>.*))?/$', PersonDetailView.as_view(), name='organization-network-person-detail'),    
    url('^profile/(?P<username>.*)/$', PersonDetailView.as_view(), name='profile'),
    url('^persons/$', PersonListView.as_view(), name='organization-network-person-list'),
    url('^person-list-block-autocomplete/$', permission_required('person.can_edit')(PersonListBlockAutocompleteView.as_view(create_field='title')), name='person-list-block-autocomplete'),
    url('^person-autocomplete/$', permission_required('person.can_edit')(PersonAutocompleteView.as_view()), name='person-autocomplete'),

    url('^network/$', OrganizationListView.as_view(), name='network'),

    url('^organization-linked-list-autocomplete/$',  permission_required('organization.can_edit')(OrganizationLinkedListView.as_view()), name='organization-linked-list-autocomplete'),
    url('^organization-linked-autocomplete/$',  permission_required('organization.can_edit')(OrganizationLinkedView.as_view()), name='organization-linked-autocomplete'),
    url('^person-activity-autocomplete/$', PersonActivityAutocompleteView.as_view(), name='person-activity-autocomplete'),
    url('^work-packages-autocomplete/$', WorkPackageAutocompleteView.as_view(), name='work-packages-autocomplete'),

    url('^producers/submission/$', ProducerCreateView.as_view(), name='organization-producer-create'),
    url('^producers/submission/(?P<slug>.*)/validation/$', ProducerValidationView.as_view(), name='organization-producer-validation'),

    url('^producers/(?P<slug>.*)/detail/$', ProducerDetailView.as_view(), name='organization-producer-detail'),
    url('^producers/list/$', ProducerListView.as_view(), name='organization-producer-list'),

    url('^jury/list/$', JuryListView.as_view(), name='organization-jury-list'),

    url('^team/(?P<slug>.*)/members$', TeamMembersView.as_view(), name='team-members'),
    url('^team/(?P<slug>.*)/publications/$', TeamPublicationsView.as_view(), name='team-publications'),
    url('^team/(?P<slug>.*)/home/$', TeamHomeView.as_view(), name='team-publications'),


    ]

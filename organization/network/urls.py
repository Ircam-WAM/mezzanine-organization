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
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.cache import cache_page

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
from rest_framework.routers import DefaultRouter

from organization.network.views import (
        # REST Views
        PersonViewSet,

        # Monolithic views
        PersonDirectoryView,
        TimeSheetCreateCurrMonthView,
        TimeSheetCreateView,
        PersonActivityTimeSheetListView,
        PersonListView,
        PersonDetailView,
        PersonAboutView,
        PersonFollowingListView,
        PersonFollowersListView,
        PersonApplicationListView,
        ProfileEditView,
        PersonListBlockAutocompleteView,
        PersonAutocompleteView,
        PersonActivityAutocompleteView,
        PersonListBlockAutocompleteView,
        PersonAutocompleteView,
        PersonActivityAutocompleteView,
        WorkPackageAutocompleteView,
        OrganizationListView,
        OrganizationLinkedListView,
        OrganizationLinkedView,
        ProducerListView,
        ProducerCreateView,
        ProducerUpdateView,
        ProducerValidationView,
        ProducerDetailView,
        JuryListView,
        PublicNetworkData,
        PublicNetworkDataNew,
        PublicNetworkStats,
        TeamMembersView,
        TeamPublicationsView,
        DynamicContentPersonView,
)

router = DefaultRouter()
router.register(
    r"person",
    PersonViewSet,
    base_name="person"
)

timeout = 60*60*24

urlpatterns = [
    url('^directory(?:/(?P<letter>.*))?/$', PersonDirectoryView.as_view(letter="a"), name='person-directory'),
    url('^person/timesheet/declare-curr-month$', TimeSheetCreateCurrMonthView.as_view(), name='organization-network-timesheet-create-curr-month-view'),
    url('^person/timesheet/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/create/$', TimeSheetCreateView.as_view(), name='organization-network-timesheet-create-view'),
    url('^person/timesheet/$', PersonActivityTimeSheetListView.as_view(), name='organization-network-timesheet-list-view' ),

    # Persons
    url('^persons/list/$', PersonListView.as_view(), name='organization-network-person-list'),
    url('^person/(?P<slug>.*)/detail/$', PersonDetailView.as_view(), name='organization-network-person-detail'),

    # Profiles
    url('^profiles/$', PersonDetailView.as_view(), name='organization-network-profile'),
    url('^profiles/(?P<username>.*)/detail/$', PersonDetailView.as_view(), name='organization-network-profile-detail'),

    url('^profiles/(?P<slug>.*)/about/$', PersonAboutView.as_view(), name='organization-network-profile-about'),

    url('^profiles/(?P<username>.*)/following/$', PersonFollowingListView.as_view(), name='organization-network-profile-following'),
    url('^profiles/(?P<username>.*)/followers/$', PersonFollowersListView.as_view(), name='organization-network-profile-followers'),
    url('^profiles/applications/$', PersonApplicationListView.as_view(), name='organization-network-profile-applications'),
    url('^profiles/edit/$', ProfileEditView.as_view(), name='organization-network-profile-edit'),
    # url('^messages/', include('postman.urls')),

    # Person autocomplete
    url('^person-list-block-autocomplete/$', permission_required('person.can_edit')(PersonListBlockAutocompleteView.as_view(create_field='title')), name='person-list-block-autocomplete'),
    url('^person-autocomplete/$', permission_required('person.can_edit')(PersonAutocompleteView.as_view()), name='person-autocomplete'),
    url('^person-activity-autocomplete/$', PersonActivityAutocompleteView.as_view(), name='person-activity-autocomplete'),
    url('^work-packages-autocomplete/$', WorkPackageAutocompleteView.as_view(), name='work-packages-autocomplete'),

    # Network
    url('^network/$', OrganizationListView.as_view(), name='network'),

    # Organizations
    url('^organization-linked-list-autocomplete/$',  permission_required('organization.can_edit')(OrganizationLinkedListView.as_view()), name='organization-linked-list-autocomplete'),
    url('^organization-linked-autocomplete/$',  permission_required('organization.can_edit')(OrganizationLinkedView.as_view()), name='organization-linked-autocomplete'),

    # Producers
    url('^producers/$', ProducerListView.as_view(), name='organization-producer-list'),
    url('^producers/create/$', ProducerCreateView.as_view(), name='organization-producer-create'),
    url('^producers/update/$', ProducerUpdateView.as_view(), name='organization-producer-update'),
    url('^producers/(?P<slug>.*)/validate/$', ProducerValidationView.as_view(), name='organization-producer-validate'),
    url('^producers/(?P<slug>.*)/detail/$', ProducerDetailView.as_view(), name='organization-producer-detail'),

    # Jurys
    url('^jurys/$', JuryListView.as_view(), name='organization-jury-list'),

    # Map
    url('^public-network-data/$', cache_page(timeout)(PublicNetworkData.as_view()), name='organization-public-network-data'),
    url('^public-network-data-new/$', cache_page(timeout)(PublicNetworkDataNew.as_view()), name='organization-public-network-data'),
    url('^public-network-stats/$', cache_page(timeout)(PublicNetworkStats.as_view()), name='organization-public-network-stats'),

    url('^team/(?P<slug>.*)/members/$', TeamMembersView.as_view(), name='team-members'),
    url('^team/(?P<slug>.*)/publications/$', TeamPublicationsView.as_view(), name='team-publications'),

    url("^dynamic-content-person/$",  DynamicContentPersonView.as_view(), name='dynamic-content-person'),

    url(r"^api/", include((router.urls))),
]

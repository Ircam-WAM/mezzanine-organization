from __future__ import unicode_literals

import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import permission_required
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.network.views import *


urlpatterns = [
    url(r'^(?P<department>.*)/teams/$', TeamListView.as_view(), name="organization-network-team-list"),
    url(r'^person/(?P<slug>.*)/$', PersonDetailView.as_view(), name="organization-network-person-detail"),
    url("^person-list-block-autocomplete/$", permission_required('person.can_edit')(PersonListBlockAutocompleteView.as_view()), name='person-list-block-autocomplete'),
    url("^person-autocomplete/$", permission_required('person.can_edit')(PersonListView.as_view()), name='person-autocomplete'),
    ]

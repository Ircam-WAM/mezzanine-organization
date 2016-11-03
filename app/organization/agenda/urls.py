from __future__ import unicode_literals

import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.core.views import *
from organization.agenda.views import *


urlpatterns = [
    url("^%s/" % settings.EVENT_SLUG, include("mezzanine_agenda.urls")),
    url("^%s/confirmation/(?P<transaction_id>[0-9]*)$" % settings.EVENT_SLUG, ConfirmationView.as_view(), name="organization-agenda-confirmation"),
]
#

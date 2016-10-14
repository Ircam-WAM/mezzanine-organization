from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
from organization.job.views import *


_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^job-offer/(?P<slug>.*)%s$" % _slash, JobOfferDetailView.as_view(), name='organization-job-offer-detail'),
    url("^job-offer/$", JobOfferListView.as_view(), name='organization-job-offer-list'),
    url("^candidacies/$", CandidacyListView.as_view(), name='candidacies-list'),
    url("^candidacy-autocomplete/$", CandidacyAutocomplete.as_view(), name='candidacy-autocomplete'),
]

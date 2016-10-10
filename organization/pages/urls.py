from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
from organization.pages.views import *

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^$", HomeView.as_view(), name="home"),
    url("^dynamic-content-home-slider/$", permission_required('home.can_edit')(DynamicContentHomeSliderView.as_view()), name='dynamic-content-home-slider'),
    url("^dynamic-content-home-body/$",  permission_required('home.can_edit')(DynamicContentHomeBodyView.as_view()), name='dynamic-content-home-body'),
    url("^dynamic-content-home-media/$",  permission_required('page.can_edit')(DynamicContentHomeMediaView.as_view()), name='dynamic-content-home-media'),
    url("^dynamic-content-page/$",  permission_required('page.can_edit')(DynamicContentPageView.as_view()), name='dynamic-content-page'),
    url("^home/$", HomeView.as_view(), name='organization-home'),
    url("^newsletter/$", NewsletterView.as_view(), name='organization-newsletter'),
]

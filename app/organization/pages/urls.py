from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
from organization.pages.views import *

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^$", HomeView.as_view(), name="home"),
    url("^dynamic-content-home-slider/$", DynamicContentHomeSliderView.as_view(), name='dynamic-content-home-slider'),
    url("^dynamic-content-home-body/$", DynamicContentHomeBodyView.as_view(), name='dynamic-content-home-body'),
    url("^home/$", HomeView.as_view(), name='organization-home'),

]

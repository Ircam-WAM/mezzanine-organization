from __future__ import unicode_literals

import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.core.views import *

urlpatterns = [
    url(r'^displayable/(?P<slug>.*)/$', CustomDisplayableView.as_view(), name="organization-displayable"),
]

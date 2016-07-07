from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from django.conf.urls import *
from django.contribimport admin
from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = [
    urls (r'^admin/lookups/', include(ajax_select_urls)), (r'^admin/', include(admin.site.urls)),
]

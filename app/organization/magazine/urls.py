from __future__ import unicode_literals

<<<<<<< HEAD
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
=======
import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
>>>>>>> 0f089a57b9482bec7a88f169e5d5fe2688c538c4

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

<<<<<<< HEAD
from organization.magazine.views import *


urlpatterns = [
    url(r'^article/$', ArticleListView.as_view(), name="magazine-article-list"),
    url(r'^article/detail/(?P<slug>.*)/$', ArticleDetailView.as_view(), name="magazine-article-detail"),
=======

urlpatterns = [

>>>>>>> 0f089a57b9482bec7a88f169e5d5fe2688c538c4
]

from django.contrib import admin
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.core.models import *
from mezzanine.blog.models import BlogPost
from mezzanine.generic.models import ThreadedComment

admin.site.register(LinkType)

admin.site.unregister(BlogPost)
admin.site.unregister(ThreadedComment)

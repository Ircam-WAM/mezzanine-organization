from django.contrib import admin
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.core.models import *
from mezzanine.blog.models import BlogPost
from mezzanine.generic.models import ThreadedComment, Keyword


class KeywordAdmin(BaseTranslationModelAdmin):

    model = Keyword


class BaseTranslationOrderedModelAdmin(BaseTranslationModelAdmin):

    def get_fieldsets(self, request, obj = None):
        res = super(BaseTranslationOrderedModelAdmin, self).get_fieldsets(request, obj)
        for field in reversed(self.first_fields):
            for trans_field in res[0][1]['fields']:
                if field in trans_field:
                    index = res[0][1]['fields'].index(trans_field)
                    res[0][1]['fields'].insert(0, res[0][1]['fields'].pop(index))
        return res


admin.site.register(LinkType)
admin.site.unregister(BlogPost)
admin.site.unregister(ThreadedComment)
admin.site.register(Keyword, KeywordAdmin)

# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.core.models import *
from mezzanine.blog.models import BlogPost
from mezzanine.generic.models import ThreadedComment, Keyword
from mezzanine.conf import settings
from django.contrib.admin import SimpleListFilter
from organization.core.translation import *
from django.contrib.auth.admin import UserAdmin
try:
    from hijack_admin.admin import HijackUserAdmin
except ImportError:
    pass
from pprint import pprint

class KeywordAdmin(BaseTranslationModelAdmin):

    model = Keyword


class BaseTranslationOrderedModelAdmin(BaseTranslationModelAdmin):

    def get_fieldsets(self, request, obj = None):
        res = super(BaseTranslationOrderedModelAdmin, self).get_fieldsets(request, obj)
        fields = reversed(self.first_fields)
        if settings.USE_MODELTRANSLATION:
            lang = settings.LANGUAGE_CODE
            lang_fields = []
            for field in fields:
                lang_fields.append(field + '_' + lang)
            fields = lang_fields
        for field in fields:
            for trans_field in res[0][1]['fields']:
                if field in trans_field:
                    index = res[0][1]['fields'].index(trans_field)
                    res[0][1]['fields'].insert(0, res[0][1]['fields'].pop(index))
        return res


class NullListFilter(SimpleListFilter):
    """Class to filter by null or not null any field in admin"""
    def lookups(self, request, model_admin):
        return (
            ('1', 'Null', ),
            ('0', '!= Null', ),
        )

    def queryset(self, request, queryset):
        if self.value() in ('0', '1'):
            kwargs = { '{0}__isnull'.format(self.parameter_name) : self.value() == '1' }
            return queryset.filter(**kwargs)
        return queryset

if settings.DEBUG :
    class UserAdminCustom(HijackUserAdmin, UserAdmin):

        list_display = UserAdmin.list_display + ('is_active',  'is_superuser', 'last_login', 'date_joined', 'person_link', 'my_groups', 'hijack_field' )

        def person_link(self, instance):
            url = reverse('admin:%s_%s_change' %(instance.person._meta.app_label, instance.person._meta.model_name),  args=[instance.person.id] )
            return '<a href="%s" target="_blank">%s</a>' %(url, instance.person.__str__())

        person_link.allow_tags = True

        def my_groups(self, instance):
            grp_str = []
            for group in instance.groups.all():
                if group :
                    grp_str.append(group.name)
            return ", ".join(grp_str)


def null_filter(field, title_=None):
    """Helper to filter by null or not null any field in admin"""
    class NullListFieldFilter(NullListFilter):
        parameter_name = field
        title = title_ or parameter_name
    return NullListFieldFilter


admin.site.register(LinkType)
admin.site.unregister(BlogPost)
admin.site.unregister(ThreadedComment)
#admin.site.register(Keyword, KeywordAdmin)

if settings.DEBUG and settings.HIJACK_REGISTER_ADMIN:
    UserModel = get_user_model()
    admin.site.unregister(UserModel)
    admin.site.register(UserModel, UserAdminCustom)

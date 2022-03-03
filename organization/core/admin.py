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
from django.contrib.admin import SimpleListFilter
from django.urls import reverse
from mezzanine.core.admin import BaseTranslationModelAdmin, SitePermissionUserAdmin,\
    UserAdmin
from mezzanine.blog.models import BlogPost
from mezzanine.generic.models import ThreadedComment, Keyword
from mezzanine.conf import settings
from mezzanine.utils.models import get_user_model
from organization.core.models import LinkType
from django.utils.safestring import mark_safe
from django.contrib.admin import helpers

try:
    from hijack_admin.admin import HijackUserAdmin
except ImportError:
    pass


class PreventLastRecordDeletionMixin():
    """
    Prevents the deletion of a record if it is the last one
    (or the last `min_objects` ones)
    """
    def has_delete_permission(self, request, obj=None):

        if not hasattr(self, 'min_objects'):
            self.min_objects = 1

        queryset = super().get_queryset(request)

        # If we're running the bulk delete action, estimate the number
        # of objects after we delete the selected items
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
        if selected:
            queryset = queryset.exclude(pk__in=selected)

        if queryset.count() <= self.min_objects:
            # Commented because has_delete_permission() is called multiple times
            # (to render the admin templates) and causes a message flood
            # message = 'There should be at least {} object(s) left.'
            # self.message_user(request, message.format(self.min_objects))

            # FIX: it returns a 401/403 and thus quits the admin... not perfect.
            return False

        return super().has_delete_permission(request, obj)


class KeywordAdmin(BaseTranslationModelAdmin):

    model = Keyword


class BaseTranslationOrderedModelAdmin(BaseTranslationModelAdmin):

    def get_fieldsets(self, request, obj=None):
        res = super(BaseTranslationOrderedModelAdmin, self).get_fieldsets(request, obj)
        fields = reversed(self.first_fields)
        if settings.USE_MODELTRANSLATION:
            lang = settings.LANGUAGE_CODE
            lang_fields = []
            for field in fields:
                lang_fields.append(field)
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
            kwargs = {
                '{0}__isnull'.format(self.parameter_name): self.value() == '1'
            }
            return queryset.filter(**kwargs)
        return queryset


if settings.DEBUG:
    class UserAdminCustom(SitePermissionUserAdmin):

        list_display = UserAdmin.list_display + (
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined',
            'person_link',
            'my_groups',
        )

        def person_link(self, instance):
            url = reverse(
                'admin:%s_%s_change' % (
                    instance.person._meta.app_label,
                    instance.person._meta.model_name
                ),  args=[instance.person.id]
            )
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (
                url,
                instance.person.__str__()
            ))

        person_link.allow_tags = True

        def my_groups(self, instance):
            grp_str = []
            for group in instance.groups.all():
                if group:
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
admin.site.register(Keyword, KeywordAdmin)


if settings.DEBUG and settings.HIJACK_REGISTER_ADMIN:
    UserModel = get_user_model()
    admin.site.unregister(UserModel)
    admin.site.register(UserModel, UserAdminCustom)

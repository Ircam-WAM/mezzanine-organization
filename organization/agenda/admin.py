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

from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationTabularInline
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from mezzanine_agenda.models import Event, EventCategory
from mezzanine_agenda.admin import *
from organization.core.models import *
from organization.agenda.models import *
from organization.agenda.forms import *


class EventBlockInline(StackedDynamicInlineAdmin):

    model = EventBlock


class EventImageInline(TabularDynamicInlineAdmin):

    model = EventImage


class EventPlaylistInline(TabularDynamicInlineAdmin):

    model = EventPlaylist


class EventDepartmentInline(TabularDynamicInlineAdmin):

    model = EventDepartment


class EventPersonInline(TabularDynamicInlineAdmin):

    model = EventPerson


class EventLinkInline(TabularDynamicInlineAdmin):

    model = EventLink


class EventTrainingInline(StackedDynamicInlineAdmin):

    model = EventTraining


class EventPeriodInline(TabularDynamicInlineAdmin):

    model = EventPeriod


class EventRelatedTitleAdmin(TranslationTabularInline):

    model = EventRelatedTitle


class EventPriceDescriptionAdmin(TranslationTabularInline):

    model = EventPriceDescription


class CustomEventPriceAdmin(BaseTranslationModelAdmin):

    inlines = [EventPriceDescriptionAdmin,]


class DynamicContentEventInline(TabularDynamicInlineAdmin):

    model = DynamicContentEvent
    form = DynamicContentEventForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )

class EventParentFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('is parent')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_parent'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('True', _('True')),
            ('False', _('False')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'True':
            return queryset.filter(parent__isnull=True)
        if self.value() == 'False':
            return queryset.exclude(parent__isnull=True)


class CustomEventAdmin(EventAdmin):
    """
    Admin class for events.
    """
    def is_parent(self, instance):
        event_is_parent = False
        if instance.parent is None:
            # self.allow_tags = True
            event_is_parent = '<div style="width:100%%; height:100%%; background-color:orange;">True</div>'
        return event_is_parent

    fieldsets = deepcopy(EventAdminBase.fieldsets)
    exclude = ("short_url", )
    is_parent.allow_tags = True
    list_display = ["title", "start", "end", "user", "status", "is_parent","admin_link"]
    if settings.EVENT_USE_FEATURED_IMAGE:
        list_display.insert(0, "admin_thumb")
    list_filter = deepcopy(DisplayableAdmin.list_filter) + ("location", "category", EventParentFilter)
    inlines = [EventPeriodInline, EventBlockInline, EventImageInline, EventDepartmentInline,
                EventPersonInline, EventLinkInline, EventPlaylistInline, EventTrainingInline,
                EventRelatedTitleAdmin, DynamicContentEventInline]


    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class CustomEventCategoryAdmin(BaseTranslationModelAdmin):

    pass


class EventPublicTypeAdmin(BaseTranslationModelAdmin):

    model = EventPublicType


class EventTrainingLevelAdmin(BaseTranslationModelAdmin):

    model = EventTrainingLevel



admin.site.unregister(Event)
admin.site.unregister(EventPrice)
admin.site.unregister(EventCategory)
admin.site.register(EventPublicType, EventPublicTypeAdmin)
admin.site.register(EventTrainingLevel, EventTrainingLevelAdmin)
admin.site.register(Event, CustomEventAdmin)
admin.site.register(EventCategory, CustomEventCategoryAdmin)
admin.site.register(EventPrice, CustomEventPriceAdmin)

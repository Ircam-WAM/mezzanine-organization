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
from mezzanine.utils.static import static_lazy as static

from modeltranslation.admin import TranslationTabularInline
from mezzanine.core.admin import StackedDynamicInlineAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin,\
    BaseTranslationModelAdmin, TabularDynamicInlineAdmin
from mezzanine_agenda.models import Event, EventCategory, Season, EventPrice
from mezzanine_agenda.admin import EventAdmin, EventAdminBase
from organization.agenda.models import EventBlock, EventImage, EventPlaylist,\
    EventDepartment, EventPersonListBlockInline, EventLink, EventTraining,\
    EventPeriod, EventRelatedTitle, EventPriceDescription, DynamicContentEvent,\
    DynamicMultimediaEvent, EventPublicType, EventTrainingLevel
from organization.agenda.forms import EventPersonListForm, DynamicContentEventForm,\
    DynamicMultimediaEventForm


class EventBlockInline(StackedDynamicInlineAdmin):

    model = EventBlock


class EventImageInline(TabularDynamicInlineAdmin):

    model = EventImage


class EventPlaylistInline(TabularDynamicInlineAdmin):

    model = EventPlaylist


class EventDepartmentInline(TabularDynamicInlineAdmin):

    model = EventDepartment


class EventPersonAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = EventPersonListBlockInline
    exclude = ("title", "description")
    form = EventPersonListForm


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

    inlines = [EventPriceDescriptionAdmin, ]
    list_display = ['value', 'description']

    def description(self, instance):
        desc = ""
        if hasattr(instance, "event_price_description"):
            desc = instance.event_price_description.description
        return desc


class DynamicContentEventInline(TabularDynamicInlineAdmin):

    model = DynamicContentEvent
    form = DynamicContentEventForm


class DynamicMultimediaEventInline(TabularDynamicInlineAdmin):

    model = DynamicMultimediaEvent
    form = DynamicMultimediaEventForm


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


class SeasonFilter(admin.SimpleListFilter):

    title = _('Seasons')
    parameter_name = 'seaon'

    def lookups(self, request, model_admin):
        seasons = Season.objects.all()
        season_lookups = ()
        for season in seasons:
            season_lookups = season_lookups + ((str(season.start.year), season.title),)
        return season_lookups

    def queryset(self, request, queryset):

        if self.value():
            season = Season.objects.get(start__year=self.value())
            return queryset.filter(start__range=[season.start, season.end])


class CustomEventAdmin(EventAdmin):
    """
    Admin class for events.
    """
    def is_parent(self, instance):
        event_is_parent = False
        if instance.parent is None:
            # self.allow_tags = True
            event_is_parent = '<div style="width:100%%; height:100%%;'
            'background-color:orange;">True</div>'
        return event_is_parent

    search_fields = ['title', 'external_id']
    fieldsets = deepcopy(EventAdminBase.fieldsets)
    exclude = ("short_url",)
    is_parent.allow_tags = True
    list_display = [
        "title",
        "start",
        "end",
        "external_id",
        "user",
        "status",
        "is_parent",
        "admin_link"
    ]
    if settings.EVENT_USE_FEATURED_IMAGE:
        list_display.insert(0, "admin_thumb")
    list_filter = deepcopy(
        DisplayableAdmin.list_filter
    ) + (
        "location",
        "category",
        EventParentFilter,
        SeasonFilter
    )
    inlines = [
        EventPeriodInline,
        EventBlockInline,
        EventImageInline,
        EventDepartmentInline,
        EventPersonAutocompleteInlineAdmin,
        EventLinkInline,
        EventPlaylistInline,
        DynamicMultimediaEventInline,
        EventTrainingInline,
        EventRelatedTitleAdmin,
        DynamicContentEventInline
    ]

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = super(CustomEventAdmin, self).get_readonly_fields(
            request,
            obj=None
        )
        if not request.user.is_superuser and 'user' not in self.readonly_fields:
            self.readonly_fields += ('user',)
        return self.readonly_fields

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


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

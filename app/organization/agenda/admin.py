from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

from mezzanine_agenda.models import Event
from mezzanine_agenda.admin import *

from organization.core.models import *
from organization.agenda.models import *


class EventBlockInline(StackedDynamicInlineAdmin):

    model = EventBlock


class EventImageInline(TabularDynamicInlineAdmin):

    model = EventImage


class EventAudioInline(StackedDynamicInlineAdmin):

    model = EventAudio


class EventVideoInline(StackedDynamicInlineAdmin):

    model = EventVideo


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


class CustomEventAdmin(EventAdmin):
    """
    Admin class for events.
    """

    fieldsets = deepcopy(EventAdminBase.fieldsets)
    exclude = ("short_url", )
    list_display = ["title", "start", "end", "user", "status", "admin_link"]
    if settings.EVENT_USE_FEATURED_IMAGE:
        list_display.insert(0, "admin_thumb")
    list_filter = deepcopy(DisplayableAdmin.list_filter) + ("location", "category")
    inlines = [EventPeriodInline, EventBlockInline, EventImageInline, EventDepartmentInline, EventPersonInline,
                EventLinkInline, EventAudioInline, EventVideoInline, EventTrainingInline]

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class EventPublicTypeAdmin(BaseTranslationModelAdmin):

    model = EventPublicType


class EventTrainingLevelAdmin(BaseTranslationModelAdmin):

    model = EventTrainingLevel



admin.site.unregister(Event)
admin.site.register(EventPublicType, EventPublicTypeAdmin)
admin.site.register(EventTrainingLevel, EventTrainingLevelAdmin)
admin.site.register(Event, CustomEventAdmin)

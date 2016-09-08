from modeltranslation.translator import translator, register, TranslationOptions

from organization.agenda.models import *


@register(EventBlock)
class EventBlockTranslationOptions(TranslationOptions):

    fields = ()


@register(EventImage)
class EventImageTranslationOptions(TranslationOptions):

    fields = ()


@register(EventDepartment)
class EventDepartmentTranslationOptions(TranslationOptions):

    fields = ()

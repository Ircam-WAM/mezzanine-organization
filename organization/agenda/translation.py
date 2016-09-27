from modeltranslation.translator import translator, register, TranslationOptions

from organization.agenda.models import *


@register(EventBlock)
class EventBlockTranslationOptions(TranslationOptions):

    fields = ()


@register(EventImage)
class EventImageTranslationOptions(TranslationOptions):

    fields = ()


@register(EventAudio)
class EventAudioTranslationOptions(TranslationOptions):

    fields = ()


@register(EventVideo)
class EventVideoTranslationOptions(TranslationOptions):

    fields = ()


@register(EventDepartment)
class EventDepartmentTranslationOptions(TranslationOptions):

    fields = ()


@register(EventPerson)
class EventPersonTranslationOptions(TranslationOptions):

    fields = ()


@register(EventLink)
class EventPersonTranslationOptions(TranslationOptions):

    fields = ()

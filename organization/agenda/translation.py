from modeltranslation.translator import translator, register, TranslationOptions

from organization.agenda.models import *


@register(EventBlock)
class EventBlockTranslationOptions(TranslationOptions):

    fields = ()


@register(EventImage)
class EventImageTranslationOptions(TranslationOptions):

    fields = ()


@register(EventPlaylist)
class EventPlaylistTranslationOptions(TranslationOptions):

    fields = ()


@register(EventDepartment)
class EventDepartmentTranslationOptions(TranslationOptions):

    fields = ()


@register(EventPerson)
class EventPersonTranslationOptions(TranslationOptions):

    fields = ()


@register(EventLink)
class EventLinkTranslationOptions(TranslationOptions):

    fields = ()


@register(EventPeriod)
class EventPeriodTranslationOptions(TranslationOptions):

    fields = ()


@register(EventTraining)
class EventTrainingTranslationOptions(TranslationOptions):

    fields = ()


@register(EventTrainingLevel)
class EventTrainingLevelTranslationOptions(TranslationOptions):

    fields = ('name',)


@register(EventPublicType)
class EventPublicTypeTranslationOptions(TranslationOptions):

    fields = ('name',)

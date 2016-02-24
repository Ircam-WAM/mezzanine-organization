from modeltranslation.translator import register, TranslationOptions

from mezzanine_agenda.models import Event
from festival.models import MetaEvent, Artist


@register(Event)
class EventTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(MetaEvent)
class MetaEventTranslationOptions(TranslationOptions):
    pass


@register(Artist)
class ArtistTranslationOptions(TranslationOptions):
    pass

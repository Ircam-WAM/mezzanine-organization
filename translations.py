from modeltranslation.translator import register, TranslationOptions

from mezzanine_agenda.models import Event, EventLocation
from festival.models import *


@register(Event)
class EventTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')

@register(EventLocation)
class EventLocationTranslationOptions(TranslationOptions):

    fields = ('description',)

@register(Artist)
class ArtistTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'bio', 'content')


@register(Video)
class VideoTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(Audio)
class AudioTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')

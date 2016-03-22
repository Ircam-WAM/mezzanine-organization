from modeltranslation.translator import register, TranslationOptions

from mezzanine_agenda.models import Event
from festival.models import *


@register(Event)
class EventTranslationOptions(TranslationOptions):

    fields = ('title', 'content')


@register(Artist)
class ArtistTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'bio', 'content')


@register(Video)
class VideoTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(Audio)
class AudioTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')

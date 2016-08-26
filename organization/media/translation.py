from modeltranslation.translator import translator, register, TranslationOptions

from organization.media.models import *


@register(Video)
class VideoTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(Audio)
class AudioTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(PageVideo)
class PageVideoTranslationOptions(TranslationOptions):

    pass

@register(PageAudio)
class PageAudioTranslationOptions(TranslationOptions):

    pass

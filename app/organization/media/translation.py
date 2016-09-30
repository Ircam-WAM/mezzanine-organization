from modeltranslation.translator import translator, register, TranslationOptions

from organization.media.models import *


@register(Video)
class VideoTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(Audio)
class AudioTranslationOptions(TranslationOptions):

        fields = ('title', 'description',)


@register(Playlist)
class PlaylistTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(MediaCategory)
class MediaCategoryTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)

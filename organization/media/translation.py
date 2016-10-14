from modeltranslation.translator import translator, register, TranslationOptions

from organization.media.models import *


@register(Media)
class MediaTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(MediaTranscoded)
class MediaTranscodedTranslationOptions(TranslationOptions):

    fields = ()


@register(Playlist)
class PlaylistTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(PlaylistMedia)
class PlaylistMediaTranslationOptions(TranslationOptions):

    fields = ()


@register(MediaCategory)
class MediaCategoryTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)

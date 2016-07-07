from modeltranslation.translator import register, TranslationOptions

from organization.festival.models import *

@register(Artist)
class ArtistTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'bio', 'content')

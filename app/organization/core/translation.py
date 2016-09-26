from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from mezzanine.generic.models import Keyword
from organization.core.models import *



@register(Keyword)
class KeywordTranslationOptions(TranslationOptions):

    fields = ('title',)

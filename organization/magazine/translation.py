from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from modeltranslation.translator import TranslationOptions
from mezzanine.core.translation import (TranslatedSlugged,
                                        TranslatedDisplayable,
                                        TranslatedRichText)
from organization.magazine.models import Article

@register(Article)
#class ArticleTranslationOptions(TranslatedDisplayable, TranslatedRichText):
class ArticleTranslationOptions(TranslationOptions):

    fields = ('sub_title',)

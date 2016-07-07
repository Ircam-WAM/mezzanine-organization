from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from custom.models import BasicPage

# @register(SubTitle)
# class SubTitleTranslationOptions(TranslationOptions):
#
#     fields = ('sub_title',)

@register(BasicPage)
class BasicPageTranslationOptions(TranslationOptions):

    fields = ('sub_title',)

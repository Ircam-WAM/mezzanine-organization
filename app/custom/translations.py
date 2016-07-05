from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from .models import BasicPage


@register(BasicPage)
class EventTranslationOptions(TranslationOptions):

    fields = ('sub_title',)

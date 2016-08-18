from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from organization.pages.models import *

@register(Home)
class HomeTranslationOptions(TranslationOptions):

    pass

@register(DynamicContentHomeSlider)
class DynamicContentHomeSliderOptions(TranslationOptions):

    pass

@register(DynamicContentHomeBody)
class DynamicContentHomeBodyOptions(TranslationOptions):

    pass

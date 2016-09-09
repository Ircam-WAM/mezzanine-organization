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


@register(CustomPage)
class CustomPageTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content')


@register(PageBlock)
class PageBlockTranslationOptions(TranslationOptions):

    fields = ('title', 'content')


@register(PageImage)
class PageImageTranslationOptions(TranslationOptions):

    fields = ('description',)


@register(PageVideo)
class PageVideoTranslationOptions(TranslationOptions):

    pass


@register(PageAudio)
class PageAudioTranslationOptions(TranslationOptions):

    pass

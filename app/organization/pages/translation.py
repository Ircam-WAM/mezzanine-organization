from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from organization.pages.models import *


@register(Home)
class HomeTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentHomeSlider)
class DynamicContentHomeSliderTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentHomeBody)
class DynamicContentHomeBodyTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentHomeMedia)
class DynamicContentHomeMediaTranslationOptions(TranslationOptions):

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


@register(PageLink)
class PageLinkTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentPage)
class DynamicContentPageTranslationOptions(TranslationOptions):

    pass


@register(LinkImage)
class LinkImageTranslationOptions(TranslationOptions):

    pass

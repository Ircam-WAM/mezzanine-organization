from modeltranslation.translator import translator, register, TranslationOptions

from organization.shop.models import *



@register(ProductBlock)
class ProductBlockTranslationOptions(TranslationOptions):

    fields = ['title',]


@register(ProductBlockProduct)
class ProductBlockProductTranslationOptions(TranslationOptions):

    pass


@register(PageProductBlock)
class PageProductBlockTranslationOptions(TranslationOptions):

    pass

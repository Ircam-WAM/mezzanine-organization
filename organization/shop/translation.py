from modeltranslation.translator import translator, register, TranslationOptions

from organization.shop.models import *



@register(ProductList)
class ProductListTranslationOptions(TranslationOptions):

    fields = ['title', 'description', 'content']


@register(ProductListProduct)
class ProductListProductTranslationOptions(TranslationOptions):

    pass


@register(PageProductList)
class PageProductListTranslationOptions(TranslationOptions):

    pass


@register(ProductLink)
class ProductLinkTranslationOptions(TranslationOptions):

    pass

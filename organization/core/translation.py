from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from organization.core.models import *


# @register(CustomDisplayable)
# class CustomDisplayableTranslationOptions(TranslationOptions):
#
#     pass
#
#
# @register(DisplayableImage)
# class DisplayableImageTranslationOptions(TranslationOptions):
#
#     fields = ('description',)
#
#
# @register(DisplayableLink)
# class DisplayableLinkTranslationOptions(TranslationOptions):
#
#     pass
#
#
# @register(DisplayableBlock)
# class DisplayableBlockTranslationOptions(TranslationOptions):
#
#     fields = ('title', 'content', )
#
#
# @register(CustomModel)
# class CustomModelTranslationOptions(TranslationOptions):
#
#     pass
#

# @register(ModelImage)
# class ModelImageTranslationOptions(TranslationOptions):
#
#     fields = ('description',)
#
#
# @register(ModelLink)
# class ModelLinkTranslationOptions(TranslationOptions):
#
#     pass
#
#
# @register(ModelBlock)
# class ModelBlockTranslationOptions(TranslationOptions):
#
#     fields = ('title', 'content', )

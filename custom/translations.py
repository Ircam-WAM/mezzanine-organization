# from modeltranslation.translator import translator, register, TranslationOptions
# from mezzanine.pages.models import Page, RichTextPage, Link
# from mezzanine.pages.translation import TranslatedRichText
# from mezzanine.forms.models import Form
# from mezzanine.galleries.models import Gallery
#
# # @register(RichText)
# # class RichTextTranslationOptions(TranslatedRichText):
# #
# #     fields = ('sub_title')
#
# # print(RichTextPage._meta.get_fields())
# # print('///////////////////////////')
# class TranslatedInjectedRichText(TranslatedRichText):
#     fields = ('sub_title',)
#
# translator.unregister(RichTextPage)
#
# translator.register(RichTextPage, TranslatedInjectedRichText)


from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from .models import BasicPage


@register(BasicPage)
class EventTranslationOptions(TranslationOptions):

    fields = ('sub_title',)
